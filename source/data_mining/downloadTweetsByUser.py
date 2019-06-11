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
import argparse

# Inspired by https://medium.com/@wilamelima/mining-twitter-for-sentiment
# -analysis-using-python-a74679b85546

def getTweetsByUser(user, outputPath = None, maxTweets = 10, verbose = True):

    ## Pull in keys from your environment
    CONSUMER_KEY    = os.environ['TWITTER_CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
    
    ACCESS_TOKEN  = os.environ['TWITTER_ACCESS_TOKEN']
    ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']
    
    # Setup access API
    def connect_to_twitter_OAuth():
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        
        api = tweepy.API(auth)
        return api
     
    # Create API object
    api = connect_to_twitter_OAuth()
    
    # Make a list of tuples.    
    tweets = [(x.text, str(x.created_at)) for x in
              tweepy.Cursor(api.user_timeline, id = user).items(maxTweets)]

    
    # Convert to JSON
    tweets_json = json.dumps(tweets)

    if outputPath:
        outputPath = os.path.join(outputPath, user + '.json')
    else:
        outputPath = os.path.join('.', user + '.json')

    with open(outputPath, 'w') as file:
        json.dump(tweets_json, file)

    # Notify the human
    if verbose:
        print('Retrieved',len(tweets), 'tweets for',
              user + '. Wrote to', outputPath + '.')

# If I'm being run as a script... otherwise just export getTweetsByUser. 
if __name__ == '__main__':

        ######
        # Create command line argument parser, populate, and parse
        parser = argparse.ArgumentParser(description=
                     "Retrieve the tweets of a Twitter user and write to a json file."
                     "  TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, "
                     "TWITTER_ACCESS_TOKEN, and TWITTER_ACCESS_SECRET must be valid "
                     "environment variables containing Twitter API credentials."
                     "Requires tweepy in PYTHONPATH. ")
        
        parser.add_argument('TwitterHandle', type=str,
                            help="The user whose tweets you'd like to retrieve.")
        
        parser.add_argument('-p','--outputDirectory', type=str, default = '.',
                             help="Where to write output json if not PWD.")
        
        parser.add_argument('-n','--numMaxTweets', type=str, default = '10',
                             help="What's the largest number of tweets to retriecve?")
        
        parser.add_argument('-v', '--verbose', action="count", default=1,
                             help="Suppress status messages.")
        
        args = parser.parse_args()
        #####
        
        if args.verbose:
            print('Getting (max: '+args.numMaxTweets+') tweets from '
                   + args.TwitterHandle+'.')
        
        if os.path.isdir(args.outputDirectory):
            if args.verbose:
                print('Path '+ args.outputDirectory +' exists.')
        else:
            if args.verbose:
                print("Path doesn't exist; creating"+args.outputDirectory+".")
            os.makedirs(args.outputDirectory)
        
              
        getTweetsByUser('@StephenAtHome',
                        maxTweets = int(args.numMaxTweets),
                        outputPath = args.outputDirectory,
                        verbose = args.verbose )