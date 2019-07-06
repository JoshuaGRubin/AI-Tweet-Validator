#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retrieves the project configuration regardless of PWD.

June, 2019
@author: Joshua Rubin
"""

import os
import json

RELATIVE_CONFIG_PATH = "../../configs/config.json" 

def get_config(config_path = None):
    """Retrives the project configuration from the default location unless
    otherwise specified.
    
    Args:

    config_path (str): The absoluted path to a configuration file. Will
    default to the standard location, <project>/configs/config.json.

    Returns:

    (dictionary): Contents of the config file with paths made absolute based
        on the config file's location.
    """
    # Using the default config... based on relative path above.
    # Make sure it resolves properly, regardless of PWD.
    if not config_path:
        # Compute absolute path to config file
        config_path = os.path.abspath(
                            os.path.join(
                                os.path.dirname(os.path.realpath(__file__)),
                                RELATIVE_CONFIG_PATH))

    with open(config_path, 'r') as file:
        config =  json.loads(file.read())

    config_file_dir = os.path.dirname(config_path)

    # Turn relative paths from config file into absolute paths in place.
    for k in config.keys():
        if '_path' in k:
            config[k] = os.path.abspath(os.path.join(config_file_dir,
                                                     config[k]))

    return config

get_config()