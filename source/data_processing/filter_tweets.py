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
    inputDirectory:  where to look for files starting with @ containing raw
                     tweets
    outputDirectory: where to deposit identically named files with filters
                     applied
    filters:         list of reg. expressions whose matches will be removed
    """

    # Look for files beginning with @, i.e. twitter handles
    tweet_files = [f for f in os.listdir(input_directory) if f[0]=='@']
        
    for file_name in tweet_files:
        input_file_path  = os.path.join(input_directory_path, file_name)
        output_file_path = os.path.join(output_directory_path, file_name)
        filter_tweets_from_files(input_file_path, output_file_path,
                                 filters, min_tweet_characters)        

# If I'm being run as a script... otherwise just provide getTweetsByUser. 
if __name__ == '__main__':
    
    with open(CONFIG_PATH, 'r') as file:
        config =  json.loads(file.read())

    config_file_dir = os.path.dirname(os.path.abspath(CONFIG_PATH))

    input_directory  = os.path.join(config_file_dir, config['raw_data_path'])
    output_directory = os.path.join(config_file_dir,
                                    config['preprocessed_data_path'])  
    
    min_tweet_characters = int(config['min_tweet_characters'])
    
    # This is a list of regular expressions to filter out.
    
#    filters = [ r'http\S+',     # URLs
#                r'@\S+[ \t]*',  # '@*' references to other users
#                r'#\S+[ \t]*' ] # '#*' hashtags.
    
    filters = config['regexp_tweet_filters']
    
    filter_tweets_from_directories(input_directory, output_directory,
                                   filters, min_tweet_characters)