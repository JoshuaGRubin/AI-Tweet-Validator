#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Offers base class, Model, from which to derive various binary classifiers,
embedding-bassed or otherwise (e.g. TFIDF).

June, 2019
@author: Joshua Rubin
"""

class Model:
    """ Base class for binary classifier to identify fraudulent tweet.
    """
   
    def set_hyperparameters(self, params = {}):
        """ Set model hyperparameters e.g. classifier threshold.
        
        Args:
        
        params (dict): Inference-time settings (e.g. cos-sim threshold)"""
        self.params = params
