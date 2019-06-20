#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for evaluating binary classification models of tweets authenticity.

June, 2019
@author: Joshua Rubin
"""

import os
import json
import numpy as np
import pandas as pd

from sklearn.metrics import confusion_matrix

from clustered_cos_sim_model import ClusteredCosSimModel

from sklearn.model_selection import train_test_split

CONFIG_PATH = "../../config.json" 

def load_tweets_from_directory(directory_path, split_frac = 0.4,
                               random_state = None):
    """ Pull in tweet data by user from <directory_path>, shuffle, split.
        
    Args:
    directory_path (str): Location of pre-embedded json user files.
    split_frac (float): train/test split fraction. Defaults to 0.4.
    random_state (None or int): Optionally set the random seed for the shuffle.
        Defaults to None.
    
    Returns:
    tuple: train and test dataframes
    """
    frames = []
    for file in os.listdir(directory_path):
        if file[0] == '@':
            print(file)
            newFrame = pd.read_json(os.path.join(directory_path,file))
            newFrame.columns = ['tweet','date','embedding']
            newFrame['name'] = file.split('.')[0]
            frames.append(newFrame)
        
    allData = pd.concat(frames)

    return train_test_split(allData, test_size = split_frac,
                                            random_state = random_state)

def compute_confusion_matrix(model, test_data):
    """ Takes an initialized model and a DataFrame containing (at-least) an
    embedded column 'embedding' and a boolean column, 'is_fraud' indicating
    whether each embedded tweet is is fraudulent (or not written by the user
    whose corpus was used to initialize the model).
    
    Args:
    model (object): initialized model instace.
    test_data (pd.dataframe): user identity and embedded tweet columns.
    
    Returns: confusion matrix array.
    """    
    
    test_embs = test_data['embedding']
    
    predicted_fraud_list = model.infer(embedded_tweets = test_embs)
    
    is_fraud_list = test_data['is_fraud']
    
    return confusion_matrix(is_fraud_list, predicted_fraud_list,
                                           labels = [True, False])

# Helpers to compute true and false positive rates form confusion matrix
def TPR(c): return np.round(c[0,0]/(c[0,0]+c[0,1]),2)
def FPR(c): return np.round(c[1,0]/(c[1,0]+c[1,1]),2)


def evaluate_model_performance(num_clusters, thresholds,
                               config_file_dir=None, input_directory=None):
    """ Ingests a directory full of twitter data on various users and
    calculates metrics on binary classification quality 
    
    Args:
    config_file_dir (str): Override for default config file path.
    input_directory (input_directory): Override for data source directory.
    """
    with open(CONFIG_PATH, 'r') as file:
        config =  json.loads(file.read())

    # Pull standard config file if not explicitly overridden
    if not config_file_dir:
        config_file_dir = os.path.dirname(os.path.abspath(CONFIG_PATH))

    # Use config-specified input data location unless overridden 
    if not input_directory:
        input_directory  = os.path.join(config_file_dir,
                                        config['processed_data_path'])

    train_data, test_data = load_tweets_from_directory(input_directory,
                                                       random_state = 1)  

    output_TPR_FPR_by_user = {}
    output_confusion_matrix_by_user = {}
    output_confusion_matrix = {}

    for user in train_data['name'].unique():
        print(f'Evaluating model for user, {user}.')
        print('%8s %6s %6s' % ('Thresh', 'TPR', 'FPR'))

        output_TPR_FPR_by_user[user] = []
        output_confusion_matrix_by_user[user] = {}

        for model_thresh in thresholds:
            
            if model_thresh not in output_confusion_matrix:
                output_confusion_matrix[model_thresh] = np.zeros([2,2], dtype=np.int32)
            
            # Add/update a column in test_data called 'is_fraud' that is false
            # if the tweet was from <user> and true otherwise.
            test_data['is_fraud'] = (test_data['name'] != user)
        
            train_user_embs = train_data[train_data['name'] 
                                                       == user]['embedding']
            # Initialize model for this user
            cluster_cos_sim_model = ClusteredCosSimModel(embedded_corpus 
                                                          = train_user_embs,
                                                       init_params={'num_clusters':4})
            # Set model classifiaction threshold.
            cluster_cos_sim_model.set_hyperparameters({'threshold':
                                                                model_thresh})
            
            # Evaluate and tabulate model results for test set.
            conf_matrix = compute_confusion_matrix(cluster_cos_sim_model,
                                                   test_data)
            
            output_TPR_FPR_by_user[user].append((model_thresh,
                                                TPR(conf_matrix),
                                                FPR(conf_matrix)))
            
            output_confusion_matrix_by_user[user][model_thresh] = conf_matrix
            output_confusion_matrix[model_thresh] += conf_matrix
            
            # Compute true and false positive rates based on confusion matrix.
            print('%8.2f %6.2f %6.2f' % (model_thresh,
                                          TPR(conf_matrix),
                                          FPR(conf_matrix)))

    output_TPR_FPR = []
    for model_thresh in thresholds:
        output_TPR_FPR.append((model_thresh,
                               TPR(output_confusion_matrix[model_thresh]),
                               FPR(output_confusion_matrix[model_thresh])))
    

# If I'm being run as a script:
if __name__ == '__main__':
    evaluate_model_performance(4, [0.2,0.3,0.4,0.5])
