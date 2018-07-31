#!/usr/bin/python
'''
Plot PR-curve for all files (ged-output) in a specified folder
'''

import sys
import os
from os import listdir
from os.path import isfile, join, exists
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import precision_recall_curve, roc_curve, auc, average_precision_score
import csv

def get_scores(ged_output_path):
    data = pd.read_csv(ged_output_path, delim_whitespace=True, header=None, quoting=csv.QUOTE_NONE)
    if(len(data.columns) == 5):
        columns = ['token', 'error_type', 'label', 'c_prob', 'i_prob']
    elif(len(data.columns) == 4):
        columns = ['token', 'label', 'c_prob', 'i_prob']
    elif(len(data.columns) == 6):
        columns = ['token', 'confidence', 'error_type', 'label', 'c_prob', 'i_prob']
    try:
        data.columns = columns
    except ValueError:
        print('The columns in the ged-output file does not match!')
        print('Expect: ' + str(columns))
        exit()

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    i_prob = []
    actual_label = []



    for idx in range(len(data)):

        row = data.loc[idx]

        # if row['token'] == '<s>' or row['token'] == '</s>':
        #     continue

        c_prob = float(row['c_prob'].strip('c:'))
        i_prob.append(1-c_prob)
        predict = 'c' if c_prob >= 0.5 else 'i'
        actual = row['label']
        actual_label.append(actual)
        if actual == 'i' and predict == 'i':
            true_positive += 1
        elif actual == 'c' and predict == 'c':
            true_negative += 1
        elif actual == 'c' and predict == 'i':
            false_positive += 1
        elif actual == 'i' and predict == 'c':
            false_negative += 1
        else:
            raise Expection


    counted_token = true_positive+true_negative+false_positive+false_negative
    if true_positive+false_positive != 0:
        p = true_positive / (true_positive+false_positive)
    else:
        p = 0
    if true_positive+false_negative != 0:
        r = true_positive / (true_positive+false_negative)
    else:
        r = 0
    if p != 0 or r != 0:
        f1 = 2 * (p*r)/(p+r)
        f05 = 1.25 * (p*r)/(0.25*p + r)
    else:
        f1 = 0
        f05 = 0
    accuracy = (true_positive+true_negative)/counted_token

    scores = {'total_token': len(data),
             'counted_token': counted_token,
             'p': p, 'r': r,
             'f1': f1, 'f05': f05,
             'accuracy': accuracy,
             'i_prob': i_prob,
             'actual_label': actual_label}
    return scores

def print_scores(scores):

    print('----------------------------------------------------------')
    print('Total Token:   {:d}'.format(scores['total_token']))
    print('Counted Token: {:d}'.format(scores['counted_token']))
    print('Precision:     {:.1f}%'.format(scores['p']*100))
    print('Recall:        {:.1f}%'.format(scores['r']*100))
    print('F1 score:      {:.1f}%'.format(scores['f1']*100))
    print('F0.5 score:    {:.1f}%'.format(scores['f05']*100))
    print('Accuracy:      {:.1f}%'.format(scores['accuracy']*100))
#     print('----------------------------------------------------------')

def plot_precision_reall_curve_multiple(scores_arr, name_arr, exp_path):

    plt.figure()
    for scores,name in zip(scores_arr,name_arr):
        preds = scores['i_prob']
        actual_label = scores['actual_label']

        precisions = []
        recalls = []

        for threshold in np.linspace(0,0.95,20):
            true_pos = 0
            true_neg = 0
            false_pos = 0
            false_neg = 0
            for pred, label in zip(preds, actual_label):
                if(pred > threshold):
                    if(label == 'i'):
                        true_pos += 1
                    else: # correct
                        false_pos += 1
                else: # pred < threshold
                    if(label == 'i'):
                        false_neg += 1
                    else:
                        true_neg += 1
            try:
                precision = true_pos / (true_pos+false_pos)
            except ZeroDivisionError:
                precision = 0
            try:
                recall = true_pos / (true_pos+false_neg)
            except ZeroDivisionError:
                recall = 0
            precisions.append(precision)
            recalls.append(recall)

        plt.plot(recalls, precisions, '.-', label=name)

    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title("Precision-Recall curve")
    plt.ylim([0.0, 1.0])
    plt.xlim([0.0, 1.0])
    plt.legend()
    save_path = exp_path + '/pr-curve.png'
    plt.savefig(save_path)
    # plt.show()



def main():

    ged_out_path = sys.argv[1]

    files = [join(ged_out_path, f) for f in listdir(ged_out_path) if (isfile(join(ged_out_path, f))) and '.exc' not in f]
    print(files)
    files.sort()
    scores_arr = []
    exp_path = os.path.dirname(ged_out_path)
    name_arr = [os.path.basename(f) for f in files]

    for i, file in enumerate(files):
        scores = get_scores(file)
        print('----------------------------------------------------------')
        print(file)
        print_scores(scores)
        scores_arr.append(scores)

    plot_precision_reall_curve_multiple(scores_arr,name_arr,exp_path)


if __name__ == '__main__':
    print(__doc__)
    main()
