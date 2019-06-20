#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corpus averaged, cosine-similarity-based binary classification model. 

June, 2019
@author: Joshua Rubin
"""

import numpy as np
from sklearn.cluster import KMeans
from base_model import Model

class ClusteredCosSimModel(Model):
    """ Derives a model that characterizes the corpus with a single normalized
        mean vector at initialization.  Inference is performed by cosine
        similarity with a threshold to produce true for inconsistent/fraudulent
        and false for consistent/authentic.
    """
    def __init__(self, corpus=None, embedded_corpus=None, init_params = {'num_clusters':1}):
        """ Requires a pre-embedded corpus passed in through <embedded_corpus>.
        """
        if embedded_corpus is None:
            raise Exception('Sorry, this model requires an embedded_corpus.')

        # Default setting; change with set_hyperparameter on base-class
        self.params = {'threshold':0.3}
                   
        kmeans = KMeans(n_clusters=init_params['num_clusters'], random_state=0).fit(
                                     np.asarray([x for x in embedded_corpus]))
        
        
        self.user_clusters = [cluster/np.sqrt(np.inner(cluster,cluster))
                                      for cluster in kmeans.cluster_centers_]
    

        
    def infer(self, tweets=None, embedded_tweets=None):
        """ Computes cosine similarity of average corpus characterization
            and input embedded tweet.  Must (for now) pass a pre-embedded
            list of tweets to <embedded_tweets>.
            
            Return value:
            Array of true/false values corresponding to fraud/authentic.
        """
        
        predictions = []
        
        for tweet in embedded_tweets:
            for cluster in self.user_clusters:
                similarity = np.inner(cluster, np.asarray(tweet))
                if similarity > self.params['threshold']:
                    predictions.append(False)
                    break
            else:
                predictions.append(True)
                                                      
        return predictions