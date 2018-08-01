import numpy as np
import pandas as pd
import sys
import os
import csv
import string

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

punc_set = set(string.punctuation)

# TODO:
# when reading a file => need to have Recall_overall & Recall_ASR

class GedOutParser(object):
    def __init__(self, columns=['token', 'error_type', 'label', 'c_prob', 'i_prob']):
        self.columns = columns
        self.num_columns = len(columns)
        self.scores = []
        self.names = []
        self.paths = []
        self.counter = 0

    def precision_recall(self, i_probs, labels):
        precisions = []
        recalls = []
        f05_scores = []
        for threshold in np.linspace(0,0.95,20):
            true_pos = 0
            true_neg = 0
            false_pos = 0
            false_neg = 0
            for i_prob, label in zip(i_probs, labels):
                if(i_prob > threshold):
                    if(label == 'i'):
                        true_pos += 1
                    else: # correct
                        false_pos += 1
                else: # i_prob < threshold
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

        for p, r in zip(precisions, recalls):
            if p != 0 or r != 0:
                f05 = 1.25 * (p*r)/(0.25*p + r)
            else:
                f05 = 0
            f05_scores.append(f05)

        # This P, R, F05 are at the operating point
        # e.g. the point at which F0.5 is the highest
        F05 = max(f05_scores)
        idx = f05_scores.index(F05)
        P = precisions[idx]
        R = recalls[idx]

        return {"P": P, "R": R, "F05": F05,
                "precisions": precisions, "recalls": recalls}

    def read(self, path, name=None, skip_options=[]):
        data = pd.read_csv(path, delim_whitespace=True, header=None, quoting=csv.QUOTE_NONE)
        assert(self.num_columns == len(data.columns))
        data.columns = self.columns

        self.counter += 1
        self.paths.append(path)
        if name != None:
            self.names.append(name)
        else:
            self.names.append('file'+str(self.counter))

        i_probs = []
        labels = []
        for idx in range(len(data)):

            row = data.loc[idx]

            if 1 in skip_options: # do not score '.'
                if row['token'] == '.':
                    continue
            if 2 in skip_options: # do not score punctuation
                if row['token'] in punc_set:
                    continue

            i_prob = float(row['i_prob'].strip('i:'))
            i_probs.append(i_prob)
            labels.append(row['label'])

        total = len(data)
        count = len(labels)
        i_count = 0
        for label in labels:
            if label == 'i':
                i_count += 1
        pr_dict = self.precision_recall(i_probs, labels)

        score = {'total': total,
                'count': count,
                'i_count': i_count,
                'P': pr_dict['P'],
                'R': pr_dict['R'],
                'F05': pr_dict['F05'],
                'precisions': pr_dict['precisions'],
                'recalls': pr_dict['recalls']}

        self.scores.append(score)

    def get_index(self):
        for i in range(self.counter):
            print("index:{}, name:{}, path:{}".format(i, self.names[i], self.paths[i]))

    def plot_pr_curves(self, indices=None, savepath=None):
        plt.figure()
        if indices == None:
            indices = range(self.counter)

        for i in indices:
            plt.plot(self.scores[i]['recalls'], self.scores[i]['precisions'],
                    '.-', label=self.names[i])

        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title("Precision-Recall curve")
        plt.ylim([0.0, 1.0])
        plt.xlim([0.0, 1.0])
        plt.legend()

        if savepath == None:
            plt.show()
        else:
            plt.savefig(savepath)

    def print_scores(self, indices=None):
        if indices == None:
            indices = range(self.counter)
        for i in indices:
            score = self.scores[i]
            print('----------------------------------------------------------')
            print('Name: {}'.format(self.names[i]))
            print('Path: {}'.format(self.paths[i]))
            print('----------------------------------------------------------')
            print('total:   {:d}'.format(score['total']))
            print('count:   {:d}'.format(score['count']))
            print('i_count: {:d}'.format(score['i_count']))
            print('P:       {:.1f}%'.format(score['P']*100))
            print('R:       {:.1f}%'.format(score['R']*100))
            print('F0.5:    {:.1f}%'.format(score['F05']*100))
