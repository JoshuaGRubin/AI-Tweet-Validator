#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retreives tweets from all the users specified in the config file at CONFIG_PATH

June, 2019
@author: Joshua Rubin
"""

import os
import json
from tweetvalidator.data_processing import get_tweets_by_user

CONFIG_PATH = "../../configs/config.json" 

with open(CONFIG_PATH, 'r') as file:
    config =  json.loads(file.read())

config_file_dir = os.path.dirname(os.path.abspath(CONFIG_PATH))

output_directory = os.path.join(config_file_dir,
                                config['raw_data_path'])  

twitter_users_to_fetch = config['twitter_users']

max_tweets_per_user = config['max_tweets_per_user']

if not os.path.isdir(output_directory):
    print(f"Path doesn't exist; creating {output_directory}.")
    os.makedirs(output_directory)
    
for user in twitter_users_to_fetch:
    print(user)
    get_tweets_by_user(user,
                       maxTweets = max_tweets_per_user,
                       output_path = output_directory)
    