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
MODULE_URL  = "https://tfhub.dev/google/universal-sentence-encoder/2"

class SentenceEncoder:
    """ Encapsulates the Universal Sentence Encoder
    
    Constructor loads the model and exposes the node 'output' which is set
    up in such a way so that the slow initialization only happens once.
    Subsequent inference happends very quickly in subsequent calls to
    embed_phrases.
    """
    def __init__(self, url = MODULE_URL):
        print('Initializing embedding model.  May take a few seconds.')
        print("(And longer if I haven't downloaded it yet.)")
        self.session = tf.Session()
        self.embed = hub.Module(url)
        self.session.run([tf.global_variables_initializer(),
                          tf.tables_initializer()])
        self.messagesPlaceholder = tf.placeholder(dtype=tf.string,
                                                  shape=[None])
        self.output = self.embed(self.messagesPlaceholder)
    
    def embed_phrases(self, phrase_list):
        """ Takes a array or list of phrases and returns an array of
            embeddings.
            
            Args:
                phrase_list (1D numpy array):  Array of phrases to encode. 
        """ 
        return self.session.run(self.output,
                                feed_dict={self.messagesPlaceholder:
                                           phrase_list})
    
    def __del__(self):
        self.session.close()

def embed_tweets_from_file(input_file_path, output_file_path, encoder = None):
    """ Read tweets from json file in <input_file_path>, embed, and output
    to <output_file_path>.
        
    Args:
        input_directory_path (str): path of input user file.
        output_directory_path (str): path to where to put user data with
            embeddings added.
    
    """    
    # If the encoder isn't passed in.  Otherwise reuse the one given.
    if not encoder:
        encoder = SentenceEncoder()
    
    with open(input_file_path, 'r') as file:
        in_data =  json.loads(file.read())
    print(f'Loaded {input_file_path}.')   
    
    data = pd.DataFrame(in_data, columns=['tweet','date'])        
    tweets = data['tweet'].values
    
    # produce a matched length vector based o the 'tweet' column of 'data' 
    message_embeddings = encoder.embed_phrases(tweets)
            
    # add the embeddings to the dataframe  
    data['embeddings'] = message_embeddings.tolist()
    print('\t' + str(len(data)), 'tweets processed.')

    # write them to destination file.        
    with open(output_file_path, 'w') as file:
        file.write(data.to_json(orient='values')) 
        
def embed_tweets_from_directories(input_directory_path, output_directory_path): 
    """ Convenience function to apply Universal Sentance Encoder to all the
    json files in an input directory.  Only files starting with '@' are
    processed.
    
    Args:
        input_directory_path (str): path to look for preprocessed user files
        output_directory_path (str): path to deposit user data with embeddings
            added.
    """      
    
    # Initialize embedding model; reuse for each file.
    sentence_encoder = SentenceEncoder()
    
    # Grab the files from the input directory
    tweet_files = [f for f in os.listdir(input_directory_path) if f[0]=='@']
        
    for file_name in tweet_files:        
        input_file_path  = os.path.join(input_directory_path, file_name)
        output_file_path = os.path.join(output_directory_path, file_name)
        embed_tweets_from_file(input_file_path,
                               output_file_path, encoder = sentence_encoder)
