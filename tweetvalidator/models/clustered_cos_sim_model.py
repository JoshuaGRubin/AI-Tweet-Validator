#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provides CousterCosSimModel which provides a variety of caracterization options
for a user's tweet corpus including single-mean and multi-cluster.

Additionally provides similarity_score and infer which take tweets and compare
with user characterization.

June, 2019
@author: Joshua Rubin
"""

import numpy as np
from base_model import Model

# This is an implementation of k-means on the hypersphere which uses
# cosine similarity rather than cartesian distance to cluster.
# https://github.com/jasonlaska/spherecluster
from spherecluster import SphericalKMeans

class ClusteredCosSimModel(Model):
    """ Derives a model that creates a mean or clustered tweet characterizaton.
        Inference is performed by cosine similarity with a threshold to produce
        true for inconsistent/fraudulent and false for consistent/authentic.
        Similarity scores used for this discrimination can optionally take
        cluster-size into account.  Clustering is performed with spherical
        k-means (which uses similarity rather than cartesian distance) to
        properly cluster normalized vectors on the unit-hypersphere.
    """
    def __init__(self, embedded_corpus=True, max_clusters=1, verbose=False):
        """ Requires a pre-embedded corpus passed in through <embedded_corpus>.
        """
 
        if not embedded_corpus:
            raise Exception('Sorry, currently requires an embedded_corpus.')
       
        self.max_clusters = max_clusters
        self.embedded_corpus = embedded_corpus
        self.verbose = verbose
        # Default setting; change with set_hyperparameter on base-class
        self.params = { 'threshold': 0.3 }   
        
        self.characterization_complete = False
     
    def characterize(self, corpus, context_corpus):
        
        # Because dataframe holds nested arrays awkwardly
        corpus = np.asarray([x for x in corpus])
                   
        kmeans = SphericalKMeans(n_clusters=self.max_clusters,
                                 random_state=0).fit(corpus)
               
        self.cluster_means = kmeans.cluster_centers_
    
        sim_sum            = np.zeros(self.max_clusters)
        self.cluster_count = np.zeros(self.max_clusters, dtype=np.int)
        self.cluster_edges = np.ones(self.max_clusters)
    
        # Compute characteristics of each cluster
        for cluster_idx, embedded_tweet in zip(kmeans.labels_, corpus):
            sim = np.inner(embedded_tweet, self.cluster_means[cluster_idx])
            
            # Tabulating the smallest similarity by cluster.
            if sim < self.cluster_edges[cluster_idx]:
                self.cluster_edges[cluster_idx] = sim
                
            self.cluster_count[cluster_idx] += 1
            sim_sum[cluster_idx] += sim

        # prune lists of single tweet clusters
        prune_list = [i for i, v in enumerate(self.cluster_count) if v == 1]
        self.cluster_count = np.delete(self.cluster_count, prune_list, axis=0)
        self.cluster_edges = np.delete(self.cluster_edges, prune_list, axis=0)
        self.cluster_means = np.delete(self.cluster_means, prune_list, axis=0)    
        sim_sum = np.delete(sim_sum, prune_list)
        
        # Mean similarity by cluster
        self.cluster_scales = sim_sum/self.cluster_count
        
        if self.verbose:
            for count, edge, mean, scale in zip(
                   self.cluster_count, self.cluster_edges,
                   self.cluster_means, self.cluster_scales):
                print(f'{count:5} {edge:5.2} {scale:5.2} {mean[:4]}')
        
        self.characterization_complete = True
    
    def similarity_score(self, embedded_tweets,
                         cluster_scaling = True):
        """ Generates similarity scores for each tweet supplied.
        
        If more than one cluster is available, the similarity score for the
        tweet is the largest score across all clusters.  To be identified as a
        legitimate tweet, we need only match one cluster.  Since a single 
        threshold will be applied, only the largest score is relevant.
        
        Args:
        embedded_tweets (2D numpy array): array of embedded of tweets.
        cluster_scaling (bool): Offset each score by the average similarity
            (i.e. cluster size) size of the cluster to which it belons.
            Defaults to true.
        
        Returns:
        1D numpy array: best similarity scores by tweet supplied.
        """
        
        embedded_tweets = np.asarray([x for x in embedded_tweets])      
                        
        if cluster_scaling:
            scores = [np.inner(mean, embedded_tweets)-scale
                      for mean, scale in zip(self.cluster_means,
                                              self.cluster_scales)]
        else:
            scores = [np.inner(mean, embedded_tweets)
                          for mean in self.cluster_means]
                  
        return np.asarray(scores).max(axis=0)
        
    def infer(self, embedded_tweets=None):
        """ Applies a threshold to a best similarity score to produce a boolean
        indicator.  Fraudulent:True.
            
            Args:
            embedded_tweets (2D numpy array): array of embedded of tweets.
        
            Returns:
            1D numpy array: true/false values corresponding to fraud/authentic.
        """
        
        tweet_scores =  self.similarity_score(embedded_tweets)       
        
        return not tweet_scores < self.params['threshold']
        
        