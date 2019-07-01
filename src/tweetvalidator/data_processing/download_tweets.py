#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gathers the tweet history of any twitter user and writes to a file.
Requires valid Twitter API credentials.
See: http://develope.twitter.com

June, 2019
@author: Joshua Rubin
"""

import os
import json
import tweepy

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

def get_tweets_by_user(user, output_path = None, max_tweets = 10):
    """ Retrives up to  <maxTweets> tweets from Twitter user, <user>.
    
        Args:
            
        user (string): Twitter handle (e.g. @MrPeanut) of a user whose tweets
            you want to download.
        output_path (string): Path to write the data.  Defaults to present
            working directory.
        max_tweets (int): The largest number for tweets to retrieve.       
    """
         
    # Create API object
    api = connect_to_twitter_OAuth()
    
    # Make a list of tuples.    
    tweets = [(x.text, str(x.created_at)) for x in
              tweepy.Cursor(api.user_timeline, id = user).items(max_tweets)]

    if output_path:
        output_path = os.path.join(output_path, user + '.json')
    else:
        output_path = os.path.join('.', user + '.json')

    with open(output_path, 'w') as file:
        json.dump(tweets, file)

    # Notify the human
    print('Retrieved',len(tweets), 'tweets for',
          user + '. Wrote to', output_path + '.')
