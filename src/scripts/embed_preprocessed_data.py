#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Takes filtered user tweet files from 'preprocessed_data_path', generates
embeddings, and writes output processed_data_path.

June, 2019
@author: Joshua Rubin
"""

from get_config import get_config
from tweetvalidator.data_processing import embed_tweets_from_directories

config = get_config()

embed_tweets_from_directories(config['preprocessed_data_path'], 
                              config['processed_data_path'])
                              