#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corpus averaged, cosine-similarity-based binary classification model. 

June, 2019
@author: Joshua Rubin
"""

import numpy as np
from base_model import Model

class AvgCosSimModel(Model):
    """ Derives a model that characterizes the corpus with a single normalized
        mean vector at initialization.  Inference is performed by cosine
        similarity with a threshold to produce true for inconsistent/fraudulent
        and false for consistent/authentic.
    """
    def __init__(self, embedded_corpus):
        """Requires a pre-embedded corpus passed in through <embedded_corpus>.
        
        Args:
        
        embedded_corpus (np.array): Array embedding vectors for user corpus
        """
           
        mean_of_embeddeded_vecs = (np.asarray([x for x in embedded_corpus])
                                    .mean(axis=0))    
        self.user_avg_embedding = mean_of_embeddeded_vecs/np.sqrt(
                                          np.inner(mean_of_embeddeded_vecs,
                                                   mean_of_embeddeded_vecs))
        # Default setting; change with set_hyperparameter on base-class
        self.params = {'threshold':0.3}

        
    def infer(self, tweets=None, embedded_tweets=None):
        """ Computes cosine similarity of average corpus characterization
            and input embedded tweet.  Must (for now) pass a pre-embedded
            list of tweets to <embedded_tweets>.
            
            Return value:
            Array of true/false values corresponding to fraud/authentic.
        """
        
        return [ np.inner(self.user_avg_embedding,
                          np.asarray(v)) < self.params['threshold']
                          for v in embedded_tweets            ]
