#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Injests similarity scores and produces an ROC/AUC graphs and data tables of
true and false positive rates by classifier threshold.

June, 2019
@author: Joshua Rubin
"""
import os
import csv
import numpy as np
import pandas as pd

# Acrobatics for OSX compatibility when running headless.
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

from sklearn.metrics import (roc_curve, roc_auc_score)
from get_config import (get_config, create_dir_if_not_there)

def generate_analysis_output(out_dir, data, legend_string, title_label = ''):
    """ Generates a ROC plot and a data table of true and false positive rates
    by classifier threshold.

    Args:
    out_dir (str): Output directory path.
    data (list of 3-tuples): Each tuple is (Name of dataset (str), list of
        scores belonging to the positive class, and list of scores belonging to
        the negative class).
    legend_string (str): The kind of thing that the name of dataset describes,
        e.g. 'model' or 'user' and drives the title of the legend.
    title_label (str): optional title to append to ROC at the top of the ROC
        plot. 
    """
    plt.figure(figsize=[8,8])
    for model, own, other in data:
        truth = np.concatenate([np.ones(len(own)), np.zeros(len(other))])
        score = np.concatenate([own, other])

        fpr, tpr, thresh = roc_curve(truth, score)
        
        auc = roc_auc_score(truth, score)

        plt.plot(fpr,tpr, label=f'{auc:.2}:{model}')

        output_df = pd.DataFrame({ 'false_pos_rate' : fpr,
                                    'true_pos_rate'  : tpr,
                                    'threshold'      : thresh})
        # For each model, save out FPR, TPR, and threshold data
        output_df.to_csv(os.path.join(out_dir,'rates_'+model+'.txt'),
                                    index=False,
                                    float_format='%14.3f',
                                    quoting=csv.QUOTE_NONE)

    plt.plot([0,1],[0,1],'k--')
    plt.xlabel('False Positive Rate', fontsize = 14)
    plt.ylabel('True Positive Rate', fontsize = 14)
    legend = plt.legend(fontsize = 12, title=f'AUC:{legend_string}')
    title = 'ROC' if not title_label else 'ROC - ' + title_label
    plt.title(title, fontsize = 14)
    plt.setp(legend.get_title(),fontsize='14')
    plt.savefig(os.path.join(out_dir,'ROC_AUC_Comparison.png'))
    plt.close()

def generate_model_comparison_by_user(input_directory, output_directory):
    models = [x for x in os.listdir(input_directory) if '.' not in x]
   
    # This loop will look across models for all users (not assuming every
    # model will have data on all users). The intent is to plot, by user,
    # whatever models are available.
    users  = []
    for model in models:
        model_users = [x for x in os.listdir(
                        os.path.join(input_directory, model)) if '.' not in x]
        users = users+model_users
    
    # dedup        
    users = list(set(users))
    
    # For each user now, let's make the plot across models.
    for user in users:
        user_out_dir = os.path.join(output_directory, user)
        create_dir_if_not_there(user_out_dir)
  
        dat = []
        for model in models:
            user_in_dir = os.path.join(input_directory, model, user)
            # if that model missing for user
            if not os.path.exists(user_in_dir):
                continue

            # Gather data by model
            dat.append(
            (model,
            pd.read_json(os.path.join(user_in_dir, 'own.json'  ))[0].values,
            pd.read_json(os.path.join(user_in_dir, 'other.json'))[0].values))
        
        generate_analysis_output(user_out_dir, dat, 'Model', user)

def generate_model_comparison(in_dir, out_dir):

    create_dir_if_not_there(output_directory)
    models = [x for x in os.listdir(input_directory) if '.' not in x]

    dat = [
    (model,
     pd.read_json(os.path.join(in_dir, model, 'own.json'  ))[0].values,
     pd.read_json(os.path.join(in_dir, model, 'other.json'))[0].values)
     for model in models ]

    generate_analysis_output(out_dir, dat, 'Model')

config = get_config()
input_directory  = config['eval_output_path']
output_directory = config['analysis_output_path']

def generate_user_comparison_by_model(input_directory, output_directory):
    models = [x for x in os.listdir(input_directory) if '.' not in x]
   
    for model in models:
        model_in_dir  = os.path.join(input_directory, model)
        model_out_dir = os.path.join(output_directory, model)
        create_dir_if_not_there(model_out_dir)

        model_users = [x for x in os.listdir(model_in_dir) if '.' not in x]

        dat = []
        for user in model_users:
            in_dir = os.path.join(model_in_dir, user)
            dat.append(
            (user,
            pd.read_json(os.path.join(in_dir, 'own.json'  ))[0].values,
            pd.read_json(os.path.join(in_dir, 'other.json'))[0].values))
        
        generate_analysis_output(model_out_dir, dat, 'User', model)

generate_model_comparison(input_directory, output_directory)
generate_model_comparison_by_user(input_directory, output_directory)
generate_user_comparison_by_model(input_directory, output_directory)