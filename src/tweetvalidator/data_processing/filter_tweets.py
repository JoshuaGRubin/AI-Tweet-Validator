#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reads raw twitter output and filters based on a list of regular expressions.

June, 2019
@author: Joshua Rubin
"""

import os
import re
import json

CONFIG_PATH = "../../config.json" 

def filter_tweets_from_files(input_file_path, output_file_path,
                             filters, min_tweet_characters):
    """ Reads tweets from a json file of [[tweet, date],...], removes
    patters matching the regexps in filters, and if more than
    <min_tweet_characters> are left, writes to the output location.
    
    Args:
        input_file_path (str):  where to look for user file
        output_file_path (str): where to deposit filtered file
        filters (list): List of reg. expressions whose matches will be removed.
        min_tweet_characters (int): Tweets with fewer characters will be
            deleted.
    """
    output_tweets = []
    print('Processing ' + input_file_path + '.', end=' ')    
   
    with open(input_file_path, 'r') as file:
        in_data =  json.loads(file.read())
    
    for tweet in in_data:
        filtered_tweet = tweet[0]
    
        # Remove text matching each of the filters sequentially.
        for reFilter in filters:
            filtered_tweet = re.sub(reFilter,'', filtered_tweet)
    
        # Trim whitespace
        filtered_tweet = filtered_tweet.strip()
        
        # Pitch if below min character threshold
        if len(filtered_tweet) >= min_tweet_characters:
            output_tweets.append([filtered_tweet, tweet[1]])
    
    print(str(len(output_tweets)), 'tweets processed.')
    
    with open(output_file_path, 'w') as file:
        json.dump(output_tweets, file) 

def filter_tweets_from_directories(input_directory_path, output_directory_path,
                 filters, min_tweet_characters):
    """Reads raw twitter output and filters based on a list of reg expressions.
    Files are json formatted lists of [tweet, date].
    
    Args:
        input_directory_path (str):  where to look for files starting with @
            containing raw tweets
        output_directory_path (str): where to deposit identically named files
            with filters applied.
        filters (list): List of reg. expressions whose matches will be removed.
        min_tweet_characters (int): Tweets with fewer characters will be
            deleted.
    """
    # Look for files beginning with @, i.e. twitter handles
    tweet_files = [f for f in os.listdir(input_directory_path) if f[0]=='@']
        
    for file_name in tweet_files:
        input_file_path  = os.path.join(input_directory_path, file_name)
        output_file_path = os.path.join(output_directory_path, file_name)
        filter_tweets_from_files(input_file_path, output_file_path,
                                 filters, min_tweet_characters)        
