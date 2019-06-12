#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reads files of [[tweet,date]] Applies Universal Sentence Encoder to to the
tweet to produce a third column with a 512 component embedding.  Writes a json
output file containing this three column data.

June, 2019
@author: Joshua Rubin
"""

import os
import json
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub

# Retrieve Universal Eentence Sncoder.
module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"
embed = hub.Module(module_url)

def embedTweets(inputDirectory, outputDirectory): 
    
    # Grab the files from the input directory
    tweetFiles = [f for f in os.listdir(inputDirectory) if f[0]=='@']
        
    for fileName in tweetFiles:   
            
        print('Loading ' + fileName + '.', end=' ')
        
        inputPath  = os.path.join(inputDirectory, fileName)

        with open(inputPath, 'r') as file:
            inData =  json.loads(file.read())
    
        data = pd.DataFrame(inData, columns=['tweet','date'])
    
        print(len(data) + ' tweets.')
    
        print('Building embedding model (may take time) and running inference.')
               
        # produce a matched length vector based o the 'tweet' column of 'data' 
        with tf.Session() as session:
          session.run([tf.global_variables_initializer(), tf.tables_initializer()])
          message_embeddings = session.run(embed(data['tweet'].values))
                
        # add the embeddings to the dataframe  
        data['embeddings'] = message_embeddings.tolist()
        
        print(str(len(data)), 'tweets processed.')
            
        outputPath = os.path.join(outputDirectory, fileName)    
    
        with open(outputPath, 'w') as file:
            file.write(data.to_json(orient='values')) 
        
# If I'm being run as a script... otherwise just provide getTweetsByUser. 
if __name__ == '__main__':
    
    inputDirectory  = '../../data/preprocessed'
    outputDirectory = '../../data/processed'
    
    embedTweets(inputDirectory, outputDirectory)