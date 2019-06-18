#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gathers the tweet history of any twitter user.
Requires valid Twitter API credentials.
See: http://develope.twitter.com

Can be imported by Python or called from the command line or Bash script

  > ./downloadTweetsByUser.py --help

for help

June, 2019
@author: Joshua Rubin
"""

import os
import json
import tweepy

CONFIG_PATH = "../../config.json" 

# Inspired by https://medium.com/@wilamelima/mining-twitter-for-sentiment
# -analysis-using-python-a74679b85546

# Setup access API
def connect_to_twitter_OAuth():
    """ Connect to Twitter API and return tweepy api object. """
    
    ## Pull in keys from your environment
    CONSUMER_KEY    = os.environ['TWITTER_CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
    
    ACCESS_TOKEN  = os.environ['TWITTER_ACCESS_TOKEN']
    ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

def get_tweets_by_user(user, output_path = None, maxTweets = 10):
    """ Retrives up to  <maxTweets> tweets from Twitter user, <user>."""
         
    # Create API object
    api = connect_to_twitter_OAuth()
    
    # Make a list of tuples.    
    tweets = [(x.text, str(x.created_at)) for x in
              tweepy.Cursor(api.user_timeline, id = user).items(maxTweets)]

    if output_path:
        output_path = os.path.join(output_path, user + '.json')
    else:
        output_path = os.path.join('.', user + '.json')

    with open(output_path, 'w') as file:
        json.dump(tweets, file)

    # Notify the human
    print('Retrieved',len(tweets), 'tweets for',
          user + '. Wrote to', output_path + '.')

# If I'm being run as a script... otherwise just export getTweetsByUser. 
if __name__ == '__main__':

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
    
        get_tweets_by_user(user,
                           maxTweets = max_tweets_per_user,
                           output_path = output_directory)