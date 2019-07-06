#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates similarity scores for a variety of models and configurations.

June, 2019
@author: Joshua Rubin
"""

CONFIG_PATH = "../../configs/config.json" 

import os
import json
from tweetvalidator.models import TFIDFModel
from tweetvalidator.models import ClusteredCosSimModel
from tweetvalidator import generate_similarity_scores


with open(CONFIG_PATH, 'r') as file:
    config =  json.loads(file.read())

config_file_dir = os.path.dirname(os.path.abspath(CONFIG_PATH))

# Use config-specified input data location unless overridden 
input_directory  = os.path.join(config_file_dir, config['processed_data_path'])
output_directory =  os.path.join(config_file_dir, config['eval_output_path'])

dir_args = {'input_directory':input_directory,
            'output_directory':output_directory}

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
