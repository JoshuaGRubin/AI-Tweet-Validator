#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Takes user tweet files from 'raw_data_path', applies filters, and writes output
to preprocessed_data_path.

June, 2019
@author: Joshua Rubin
"""

from get_config import (get_config, create_dir_if_not_there)
from tweetvalidator.data_processing import filter_tweets_from_directories

# Pull-in filter settings from global configuration.    
config = get_config()

create_dir_if_not_there(config['preprocessed_data_path'])

filter_tweets_from_directories(config['raw_data_path'],
                               config['preprocessed_data_path'],
                               config['regexp_tweet_filters'],
                                int(config['min_tweet_characters'])    )
