#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Injests similarity scores and produces an ROC/AUC graph.

June, 2019
@author: Joshua Rubin
"""
import os
import numpy as np
import pandas as pd


import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

from sklearn.metrics import (roc_curve, roc_auc_score)

from get_config import get_config
config = get_config()

input_directory  = config['eval_output_path']
output_directory = config['graph_output_path']

contents = os.listdir(input_directory)

labels = [x.split('_own.json')[0] for x in contents if '.json' in x
                                                    and 'own'  in x]

dat = [
   (pd.read_json(os.path.join(input_directory, lab + '_own.json'  ))[0].values,
    pd.read_json(os.path.join(input_directory, lab + '_other.json'))[0].values)
    for lab in labels ]

plt.figure(figsize=[8,8])

for lab, (own, other) in zip(labels, dat):
    truth = np.concatenate([np.ones(len(own)), np.zeros(len(other))])
    score = np.concatenate([own, other])

    fpr, tpr, thresh = roc_curve(truth, score)
    
    auc = roc_auc_score(truth, score)

    plt.plot(fpr,tpr, label=f'{auc:.2}:{lab}')

plt.plot([0,1],[0,1],'k--')
plt.xlabel('False Positive Rate', fontsize = 14)
plt.ylabel('True Positive Rate', fontsize = 14)
legend = plt.legend(fontsize = 12, title='AUC:Model')
plt.title('ROC', fontsize = 14)
plt.setp(legend.get_title(),fontsize='14')

plt.savefig(os.path.join(output_directory,'ROC_AUC_Comparison.png'))
