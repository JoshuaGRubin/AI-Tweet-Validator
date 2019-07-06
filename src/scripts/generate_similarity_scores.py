#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates similarity scores for a variety of models and configurations.

June, 2019
@author: Joshua Rubin
"""

import os
from get_config import get_config
config = get_config()

from tweetvalidator.models import TFIDFModel
from tweetvalidator.models import ClusteredCosSimModel
from tweetvalidator import generate_similarity_scores

dir_args = {'input_directory'  : config['processed_data_path'],
            'output_directory' : config['eval_output_path']}

input_directory = config['preprocessed_data_path']
output_directory = config['processed_data_path']

if not os.path.isdir(output_directory):
    print(f"Path doesn't exist; creating {dir_args['output_directory']}.")
    os.makedirs(dir_args['output_directory'])

print('Running term-frequency model.')
generate_similarity_scores(TFIDFModel(use_context=True),
                           'tweet', **dir_args,
                           file_prefix = 'tfidf') 

print('Running full TDIDF model.')
generate_similarity_scores(TFIDFModel(use_context=False),
                           'tweet', **dir_args,
                           file_prefix = 'tf') 

print('Running mean embedding model.')
generate_similarity_scores(ClusteredCosSimModel(max_clusters=1, verbose=False),
                           'embedding', **dir_args,
                           file_prefix = 'emb_1',
                           score_args={'cluster_scaling':False})

print('Running mean embedding model with cluster size scaling.')
generate_similarity_scores(ClusteredCosSimModel(max_clusters=1, verbose=True),
                           'embedding', **dir_args,
                           file_prefix = 'emb_1_scaled',
                           score_args={'cluster_scaling':True})

print('Running two-cluster model.')
generate_similarity_scores(ClusteredCosSimModel(max_clusters=2, verbose=False),
                           'embedding', **dir_args,
                           file_prefix = 'emb_2',
                           score_args={'cluster_scaling':False})

print('Running two-cluster model with-cluster size scaling.')
generate_similarity_scores(ClusteredCosSimModel(max_clusters=2, verbose=True),
                           'embedding', **dir_args,
                           file_prefix = 'emb_2_scaled',
                           score_args={'cluster_scaling':True})
