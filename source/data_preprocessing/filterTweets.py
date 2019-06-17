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


def filterTweets(inputDirectory, outputDirectory, filters):
    """Reads raw twitter output and filters based on a list of regular expressions.
    
    Files are json formatted lists of [tweet, date].
    inputDirectory:  where to look for files starting with @ containing raw tweets
    outputDirectory: where to deposit identically named files with filters applied
    filters:         list of reg. expressions whose matches will be removed
    """

    # Look for files beginning with @, i.e. twitter handles
    tweetFiles = [f for f in os.listdir(inputDirectory) if f[0]=='@']
        
    for filename in tweetFiles:   
        
        outputTweets = []

        print('Processing ' + filename + '.', end=' ')
        
        inputPath  = os.path.join(inputDirectory, filename)

        with open(inputPath, 'r') as file:
            inData =  json.loads(file.read())
    
        for tweet in inData:
               
            filteredTweet = tweet[0]

            # Remove text matching each of the filters sequentially.
            for reFilter in filters:
                filteredTweet = re.sub(reFilter,'', filteredTweet)

            filteredTweet = filteredTweet.strip() # Trim whitespace
            if filteredTweet:                     # If there's anything left...
                outputTweets.append([filteredTweet, tweet[1]])

        print(str(len(outputTweets)), 'tweets processed.')
        
        outputPath = os.path.join(outputDirectory, filename)    

        with open(outputPath, 'w') as file:
            json.dump(outputTweets, file) 
        

# If I'm being run as a script... otherwise just provide getTweetsByUser. 
if __name__ == '__main__':
    
    inputDirectory  = '../../data/raw'
    outputDirectory = '../../data/preprocessed'
    
    # This is a list of regular expressions to filter out.
    
    filters = [ r'http\S+',     # URLs
                r'@\S+[ \t]*',  # '@*' references to other users
                r'#\S+[ \t]*' ] # '#*' hashtags.
                
    filterTweets(inputDirectory, outputDirectory, filters)