#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Downloads tweets for users specified in 'twitter_users' field of config.json

June, 2019
@author: Joshua Rubin
"""

import os
from get_config import get_config
from tweetvalidator.data_processing import get_tweets_by_user

config = get_config()

output_directory = config['raw_data_path']

max_tweets_per_user = config['max_tweets_per_user']

if not os.path.isdir(output_directory):
    print(f"Path doesn't exist; creating {output_directory}.")
    os.makedirs(output_directory)

twitter_users_to_fetch = config['twitter_users'] 

for user in twitter_users_to_fetch:
    print(user)
    get_tweets_by_user(user,
                       max_tweets = max_tweets_per_user,
                       output_path = output_directory)
    