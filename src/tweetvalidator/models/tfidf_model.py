#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Computes similarity of tweet to user corpus using pure term-frequency (TF) or
term-frequency-inverse-document-frequency (TFIDF), in which a context-corpus
of other-user tweets are used to normalize common terms in the
characterization. 

June, 2019
@author: Joshua Rubin
"""

from .base_model import Model
from sklearn.feature_extraction.text import TfidfVectorizer

class TFIDFModel(Model):
    """ Initializez TF/TFIDF model according to the standard model idiom.
    
        Args:
        use_context (boolean): Initialize the model as either (false)
        term-frequency or (true) term-frequency-inverse-document-frequency.
    """
    def __init__(self, use_context=True):      
        # Default setting; change with set_hyperparameter on base-class
        self.params = {'threshold':0.3}
        self.use_context = use_context

    def characterize(self, corpus, context_corpus):
        """Computes TFIDF for a corpus of user tweets.  TF is computed from
        concatinated tweets.  IDF is computed in conjunction with an optional
        corpus of non-user tweets (depends on use_contxt value in constuctor). 
        
        Args:
        user_tweet_corpus (np.array): Array of text tweets by the user to model
        context_tweet_corpus (np.array): Optional array non-user tweets for
            common word normalization.  If none, skip the IDF (default:none).
        """
        if self.use_context:  # provided context vector to support IDF
            tfidf_vectorizer = TfidfVectorizer(stop_words='english',
                                                       use_idf=True)
            self.word_freq_vec = tfidf_vectorizer.fit_transform(
                [' '.join(corpus),
                 ' '.join(corpus)+' '.join(context_corpus)]
                 ).toarray()[0]
        
        else: # No context, just term frequency
            tfidf_vectorizer = TfidfVectorizer(stop_words='english',
                                               use_idf=False)
            self.word_freq_vec = tfidf_vectorizer.fit_transform(
                                [' '.join(corpus)]).toarray()[0]
    
        self.feature_names = tfidf_vectorizer.get_feature_names()
        
    def similarity_score(self, tweets):
        """ Computes similarity score of corpus characterization and input
        tweets.
        
        Args:
        tweets (1D numpy array): plaintext tweets. 
            
        Returns:
        1D numpy array: similarity scores by tweet supplied.
        """
        
        tfidf_vectorizer = TfidfVectorizer(stop_words='english', use_idf=False,
                                           vocabulary = self.feature_names)
        
        tweet_freqs = tfidf_vectorizer.fit_transform(tweets)
        
        return tweet_freqs.dot(self.word_freq_vec)

    
    def infer(self, tweets):
        """ Applies a threshold to each similarity score to produce a boolean
        indicator.  Fraudulent:True.
            
            Args:
            tweets (1D numpy array): plaintext tweets. 
        
            Returns:
            1D numpy array: true/false values corresponding to fraud/authentic.
        """        
        
        return self.similarity_score(tweets) < self.params['threshold']