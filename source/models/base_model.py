#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Offers base class, Model, from which to derive various binary classifiers,
embedding-bassed or otherwise (e.g. TFIDF).

June, 2019
@author: Joshua Rubin
"""

class Model:
    """ Base class for binary classifier to identify fraudulent tweet . """
   
    def __init__(self, corpus=None, embedded_corpus=None):
        """ Intended to accomodate both text and embedded corpuses.  Sometimes
            it's helpful to precompute the embeddings (e.g. working with the
            demo data) in the repo.  It's the derived model's job to raise
            an exception if it can't process the specified data type.
            
            A corpus (numpy array or Pandas series) must be passed-in at
            initialization.  
        """
        pass
   
    def set_hyperparameters(self, params = {}):
        """ Set model hyperparameters e.g. classifier threshold."""
        self.params = params
    
    def infer(self, tweets=None, embedded_tweets=None):
        """ Pass in a list of tweets (text or embedded if appropriate for model
            type) to test against 
        """    