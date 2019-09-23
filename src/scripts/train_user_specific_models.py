#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates similarity scores for a variety of models and configurations.

September, 2019
@author: Joshua Rubin
"""

from get_config import (get_config, create_dir_if_not_there)
config = get_config()
create_dir_if_not_there(config['eval_output_path'])

from tweetvalidator.models import RandomForestModel
from tweetvalidator import train_models

dir_args = {'input_directory'  : config['processed_data_path'],
            'output_directory' : config['eval_output_path']}

train_models(RandomForestModel(verbose=True),
            'embedding', **dir_args,
            file_prefix = 'random_forest_model')
