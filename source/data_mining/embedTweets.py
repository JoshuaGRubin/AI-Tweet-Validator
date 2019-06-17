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
MODULE_URL = "https://tfhub.dev/google/universal-sentence-encoder/2"

class SentenceEncoder:
    def __init__(self, url = MODULE_URL):
        self.session = tf.Session()
        self.embed = hub.Module(url)
        self.session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        self.messagesPlaceholder = tf.placeholder(dtype=tf.string, shape=[None])
        self.output = self.embed(self.messagesPlaceholder)
    
    def embed_phrases(self, phrase_list):
        return self.session.run(self.output, feed_dict={self.messagesPlaceholder: phrase_list})
    
    def __del__(self):
        self.session.close()
        
def embed_tweets_from_directories(input_directory_path, output_directory_path): 
    
    # Initialize embedding model.
    print('Initializing embedding model.  May take a few seconds.')
    sentence_encoder = SentenceEncoder()
    
    # Grab the files from the input directory
    tweet_files = [f for f in os.listdir(input_directory_path) if f[0]=='@']
        
    for file_name in tweet_files:   
            
        print('Loading ' + file_name + '.', end=' ')        
        input_file_path  = os.path.join(input_directory_path, file_name)
        with open(input_file_path, 'r') as file:
            in_data =  json.loads(file.read())
    
        data = pd.DataFrame(in_data, columns=['tweet','date'])    
        print('\t' + str(len(data)) + ' tweets loaded.')
               
        tweets = data['tweet'].values
        
        # produce a matched length vector based o the 'tweet' column of 'data' 
        message_embeddings = sentence_encoder.embed_phrases(tweets)
                
        # add the embeddings to the dataframe  
        data['embeddings'] = message_embeddings.tolist()
        
        print('\t' + str(len(data)), 'tweets processed.')
            
        output_path = os.path.join(output_directory_path, file_name)    
        with open(output_path, 'w') as file:
            file.write(data.to_json(orient='values')) 
        
# If I'm being run as a script... otherwise just provide getTweetsByUser. 
if __name__ == '__main__':
    
    input_directory  = '../../data/preprocessed'
    output_directory = '../../data/processed'
    
    embed_tweets_from_directories(input_directory, output_directory)