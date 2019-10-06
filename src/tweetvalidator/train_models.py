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
import pickle as pk
from sklearn.metrics import confusion_matrix
from sklearn.metrics import  precision_recall_fscore_support
from sklearn.model_selection import train_test_split

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
            newFrame = pd.read_json(os.path.join(directory_path,file))
            newFrame.columns = ['tweet','date','embedding']
            newFrame['name'] = file.split('.')[0]
            frames.append(newFrame)
        
    allData = pd.concat(frames)

    return train_test_split(allData, test_size = split_frac,
                                            random_state = random_state)

def safe_mkdir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)

def train_models(model, data_column,
                        file_prefix = '',
                        score_args = {},
                        config_file_dir=None,
                        input_directory=None,
                        negative_input_directory=None,
                        output_directory=None,
                        users = None):
    """ Ingests a model and a directory full of twitter data on various users,
        provides a classifier with both positive and negative examples for
        training, and then saves 1) a serialized classifier for each user, 2)
        a confusion matrix computed using reserved test data, and a details
        files.

    Args:
        
    model (object): An instance of a model model from this package.
    data_column (str): either 'tweet' or 'embedding' to determine what this
       function passes to the model; e.g. 'tweet' for TDIDF and 'embedding' for
       the embedding-based models.
    file_prefix (str): The prefix to use when saving out files from this run.
    score_args (dict): Keyword args to be passed into the models
        similarity_score function - e.g. to specify whether or not to
        cluster_scale.
    config_file_dir (str): Override for default config file path.
    input_directory (str): Override for data source directory.
    output_directory(str): Override for metrics output directory path.
    users (list of strings): Override input_directory contents to select
        specific users.
        
    Return:
        
    (2-tuple of arrays): Own and other similarity score arrays.
    """

    output_directory = os.path.join(output_directory, file_prefix)
    safe_mkdir(output_directory)

    train_data, test_data = load_tweets_from_directory(input_directory,
                                                    random_state = 1)  

    if negative_input_directory:
        neg_train_data, neg_test_data = load_tweets_from_directory(
                                                    negative_input_directory,
                                                    random_state = 1)  

    if users is None:
        users = train_data['name'].unique()

    for user in users:
        print(f'\tEvaluating model for {user}.')
        
        user_train_dat  = train_data[train_data['name'] == user][data_column]

        user_test_dat  = test_data[test_data['name'] == user][data_column]

        if negative_input_directory:
            print("Here")
            print(negative_input_directory)
            other_train_dat = neg_train_data[neg_train_data['name'] != user][
                                                                data_column]
            
            other_test_dat = neg_test_data[neg_test_data['name'] != user][
                                                                data_column]

        else:
            other_train_dat = train_data[train_data['name'] != user][
                                                                data_column]
            
            other_test_dat = test_data[test_data['name'] != user][data_column]

        other_test_dat = other_test_dat[:len(user_test_dat)]

        # Initialize model for this user
        model.characterize(user_train_dat, other_train_dat)
      


        user_test_pred = model.infer(user_test_dat)
        user_test_truth = np.ones(len(user_test_dat))
        # print(user_test_pred)

        other_test_pred = model.infer(other_test_dat)
        other_test_truth = np.zeros(len(other_test_dat))
        # print(len(other_test_pred))

        y_pred = np.concatenate([user_test_pred, other_test_pred])
        y_true = np.concatenate([user_test_truth, other_test_truth])
                    
        # Serialize model and save
        model_path = os.path.join(output_directory, user + "_model.pkl")
        print(model_path)
        with open(model_path, 'wb') as f:
            pk.dump(model, f)
        
        # Save confustion matrix
        cm = confusion_matrix(y_true, y_pred)
        print(cm)
        conf_matrix_path = os.path.join(output_directory,
                                        user + "_conf_mat.txt")
        with open(conf_matrix_path, 'w') as f:
            f.write(str(cm))

        # Save out some human readible stats.
        details_path = os.path.join(output_directory,
                                user + "_details.txt")
   
        print(f"TPR (for fraud ID):{cm[0,0]/(cm[0,0]+cm[0,1]):0.2f}")
        print(f"FPR               :{cm[1,0]/(cm[1,0]+cm[1,1]):0.2f}")

        pr = precision_recall_fscore_support(y_true,y_pred)[:2]

        with open(details_path, 'w') as f:
            f.write(f"{len(user_test_dat)} test tweets for {user} and others.")
            f.write('\n')
            f.write(f"TPR (for fraud ID):{cm[0,0]/(cm[0,0]+cm[0,1]):0.2f}\n")
            f.write(f"FPR               :{cm[1,0]/(cm[1,0]+cm[1,1]):0.2f}\n")
            f.write(f"Precision, recall for classes other, user:\n{str(pr)}")
             