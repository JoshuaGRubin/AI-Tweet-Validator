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

from base_model import Model
from sklearn.feature_extraction.text import TfidfVectorizer

class TFIDFModel(Model):
    """ Derives a model that characterizes the corpus with a single normalized
        mean vector at initialization.  Inference is performed by cosine
        similarity with a threshold to produce true for inconsistent/fraudulent
        and false for consistent/authentic.
    """
    def __init__(self, use_context=True):
        """Computes TFIDF for a corpus of user tweets.  TF is computed from
        concatinated tweets.  IDF is computed in conjunction with an optional
        corpus of non-user tweets. 
        
        Args:
        user_tweet_corpus (np.array): Array of text tweets by the user to model
        context_tweet_corpus (np.array): Optional array non-user tweets for
            common word normalization.  If none, skip the IDF (default:none).
        """
       
        # Default setting; change with set_hyperparameter on base-class
        self.params = {'threshold':0.3}
        self.use_context = use_context

    def characterize(self, corpus, context_corpus):        
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
        tfidf_vectorizer = TfidfVectorizer(stop_words='english', use_idf=False,
                                           vocabulary = self.feature_names)
        
        tweet_freqs = tfidf_vectorizer.fit_transform(tweets)
        
        return tweet_freqs.dot(self.word_freq_vec)

    
    def infer(self, tweets):
        """ Computes cosine similarity of average corpus characterization
            and input embedded tweet.  Must (for now) pass a pre-embedded
            list of tweets to <embedded_tweets>.
            
            Return value:
            Array of true/false values corresponding to fraud/authentic.
        """
        
        return self.similarity_score(tweets) < self.params['threshold']