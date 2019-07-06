#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Takes user tweet files from 'raw_data_path', applies filters, and writes output
to preprocessed_data_path.

June, 2019
@author: Joshua Rubin
"""

import os
from get_config import get_config
from tweetvalidator.data_processing import filter_tweets_from_directories

# Pull-in filter settings from global configuration.    
config = get_config()

input_directory = config['raw_data_path']
output_directory = config['preprocessed_data_path']

if not os.path.isdir(output_directory):
    print(f"Path doesn't exist; creating {output_directory}.")
    os.makedirs(output_directory)

filter_tweets_from_directories(input_directory,
                               output_directory,
                               config['regexp_tweet_filters'],
                                int(config['min_tweet_characters'])    )
