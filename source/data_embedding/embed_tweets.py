#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Encapsulates Universal Sentence Encoder

Provides SentenceEncoder class which keeps model resident to reduce need
for the slow model initialization, provides convenience funtion to map all
the tweets from a preprocessed directory to a processed directory, and a shell
invocation wrapper.

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
    """ Encapsulates the Universal Sentence Encoder
    
    Constructor loads the model and exposes the node 'output' which is set
    up in such a way so that the slow initialization only happens once.
    Subsequent inference happends very quickly in subsequent calls to
    embed_phrases.
    """
    def __init__(self, url = MODULE_URL):
        self.session = tf.Session()
        self.embed = hub.Module(url)
        self.session.run([tf.global_variables_initializer(),
                          tf.tables_initializer()])
        self.messagesPlaceholder = tf.placeholder(dtype=tf.string,
                                                  shape=[None])
        self.output = self.embed(self.messagesPlaceholder)
    
    def embed_phrases(self, phrase_list):
        """ Takes a array or list of phrases and returns a array of embeddings. """ 
        return self.session.run(self.output,
                                feed_dict={self.messagesPlaceholder:
                                           phrase_list})
    
    def __del__(self):
        self.session.close()
        
def embed_tweets_from_directories(input_directory_path, output_directory_path): 
    """ Convenience function to apply Universal Sentance Encoder to all the
    json files in <input_dirextory_path> and writing them to
    <output_directory_path>.
    
    Only files starting with '@' are processed.
    """      
    
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
    
#    embed_tweets_from_directories(input_directory, output_directory)