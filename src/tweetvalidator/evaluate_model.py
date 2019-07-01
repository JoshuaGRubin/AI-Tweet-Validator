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
from tfidf_model import TFIDFModel
from sklearn.model_selection import train_test_split
from clustered_cos_sim_model import ClusteredCosSimModel as EmbModel

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

# From https://stackoverflow.com/a/47626762/1306026; thanks!
class NumpyEncoder(json.JSONEncoder):
    """ Helper for JSON library to encode/decode numpy arrays.
    
    See: https://stackoverflow.com/a/47626762/1306026
    """
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def evaluate_model_performance(model, data_column,
                               file_prefix = '',
                               score_args = {},
                               config_file_dir=None,
                               input_directory=None,
                               output_directory=None,
                               users = None):
    """ Ingests a model and a directory full of twitter data on various users
    and writes two fies: one contianing similarity scores for the "own" user's
    tweets and an "other" file with scores for tweets belonging to other users.
     
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
    with open(CONFIG_PATH, 'r') as file:
        config =  json.loads(file.read())

    # Pull standard config file if not explicitly overridden
    if not config_file_dir:
        config_file_dir = os.path.dirname(os.path.abspath(CONFIG_PATH))

    # Use config-specified input data location unless overridden 
    if not input_directory:
        input_directory  = os.path.join(config_file_dir,
                                        config['processed_data_path'])
        
    if not output_directory:
        output_directory =  os.path.join(config_file_dir,
                                         config['eval_output_path'])

    train_data, test_data = load_tweets_from_directory(input_directory,
                                                       random_state = 1)  
    scores_own   = []
    scores_other = []

    if users is None:
        users = train_data['name'].unique()

    for user in users:
        print(f'Evaluating model for {user}.')
        
        user_train_dat  = train_data[train_data['name'] == user][data_column]
        other_train_dat = train_data[train_data['name'] != user][data_column]

        # Initialize model for this user
        model.characterize(user_train_dat, other_train_dat)
        
        my_test_tweets     = test_data[test_data['name'] == user][data_column]
        other_test_tweets  = test_data[test_data['name'] != user][data_column]
        
        my_scores     = model.similarity_score(my_test_tweets, **score_args)
        not_my_scores = model.similarity_score(other_test_tweets, **score_args)
             
        scores_own   = np.concatenate((scores_own,   my_scores))
        scores_other = np.concatenate((scores_other, not_my_scores))            
       
    os.makedirs(output_directory, exist_ok=True)

    out_file_path=os.path.join(output_directory, f'{file_prefix}_own.json')                     
    with open(out_file_path, 'w') as file:
        json.dump(scores_own, file, cls=NumpyEncoder) 
    
    out_file_path=os.path.join(output_directory, f'{file_prefix}_other.json') 
    with open(out_file_path, 'w') as file:
        json.dump(scores_other, file, cls=NumpyEncoder) 

    return scores_own, scores_other    

# If I'm being run as a script:
if __name__ == '__main__':

    evaluate_model_performance(EmbModel(max_clusters=1, verbose=True),
                               'embedding',
                               file_prefix = 'emb_1_scaled',
                               score_args={'cluster_scaling':True})

    evaluate_model_performance(EmbModel(max_clusters=1, verbose=False),
                               'embedding',
                               file_prefix = 'emb_1',
                               score_args={'cluster_scaling':False})
    
    evaluate_model_performance(EmbModel(max_clusters=2, verbose=True),
                               'embedding',
                               file_prefix = 'emb_2_scaled',
                               score_args={'cluster_scaling':True})

    evaluate_model_performance(EmbModel(max_clusters=2, verbose=False),
                               'embedding',
                               file_prefix = 'emb_2',
                               score_args={'cluster_scaling':False})  
    
    evaluate_model_performance(TFIDFModel(use_context=True),
                               'tweet',
                               file_prefix = 'tfidf') 
    
    evaluate_model_performance(TFIDFModel(use_context=False),
                               'tweet',
                               file_prefix = 'tf') 