#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Takes user tweet files from 'raw_data_path', applies filters, and writes output
to preprocessed_data_path.

June, 2019
@author: Joshua Rubin
"""

import os
import json
from tweetvalidator.data_processing import filter_tweets_from_directories

CONFIG_PATH = "../../configs/config.json" 

with open(CONFIG_PATH, 'r') as file:
    config =  json.loads(file.read())

config_file_dir = os.path.dirname(os.path.abspath(CONFIG_PATH))
input_directory  = os.path.join(config_file_dir, config['raw_data_path'])
output_directory = os.path.join(config_file_dir,
                                config['preprocessed_data_path'])  

# Pull-in filter settings from global configuration.    
min_tweet_characters = int(config['min_tweet_characters'])    
filters = config['regexp_tweet_filters']

filter_tweets_from_directories(input_directory, output_directory,
                               filters, min_tweet_characters)
