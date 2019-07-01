#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Takes filtered user tweet files from 'preprocessed_data_path', generates
embeddings, and writes output processed_data_path.

June, 2019
@author: Joshua Rubin
"""

import os
import json
from tweetvalidator.data_processing import embed_tweets_from_directories

CONFIG_PATH = "../../configs/config.json" 

with open(CONFIG_PATH, 'r') as file:
    config =  json.loads(file.read())

config_file_dir = os.path.dirname(os.path.abspath(CONFIG_PATH))

input_directory  = os.path.join(config_file_dir,
                                config['preprocessed_data_path'])

output_directory = os.path.join(config_file_dir,
                                config['processed_data_path'])  

embed_tweets_from_directories(input_directory, output_directory)