import numpy as np
import pandas as pd
import sys
import os
import csv
import string
from collections import OrderedDict

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
        thresholds = np.linspace(0,0.95,20)
        for threshold in thresholds:
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
        threshold = thresholds[idx]

        return {"P": P, "R": R, "F05": F05,
                "precisions": precisions, "recalls": recalls,
                'threshold': threshold}

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
                'recalls': pr_dict['recalls'],
                'threshold': pr_dict['threshold']}

        self.scores.append(score)

    def show_indices(self):
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

    def error_type_recall_rate(self, index):
        if self.num_columns <= 2:
            print("No Error Type Column")
            return

        data = pd.read_csv(self.paths[index], delim_whitespace=True, header=None, quoting=csv.QUOTE_NONE)
        data.columns = self.columns

        # if i_prob >= threshold => predict 'i'
        threshold = self.scores[index]['threshold']
        preds= []
        for idx, row in data.iterrows():
            i_prob = float(row['i_prob'].strip('i:'))
            pred = 'i' if i_prob >= threshold else 'c'
            preds.append(pred)
        data['prediction'] = preds


        # ---- error type ---- #
        # refer to www.cl.cam.ac.uk/techreports/UCAM-CL-TR-915.pdf

        print('----------------------------------------------------------')
        print('File =', self.paths[index])
        print('----------------------------------------------------------')

        major_types = ['F', 'M', 'R', 'U', 'Other']
        word_classes = ['N','V','A','D','J','T','Y','_']
        # error1 = OrderedDict({'F': OrderedDict(), 'M': OrderedDict(), 'R': OrderedDict(), 'U': OrderedDict(), 'Other': OrderedDict()})
        error1 = OrderedDict()
        for major in major_types:
            error1[major] = OrderedDict()
            for w in word_classes:
                error1[major][w] = ErrorCount()

        for idx, row in data.iterrows():
            err = row['error_type']
            label = row['label']
            pred = row['prediction']

            if label == 'c':
                continue

            # ignore the second type of error for now
            major = err[0]
            try:
                w_class = err[1]
            except IndexError:
                w_class = None

            if major in major_types: # F, M, R, U
                if w_class in word_classes: # 'N','V','A','D','J','T','Y'
                    error1[major][w_class].add(label, pred)
                else:
                    error1[major]['_'].add(label,pred)
            else:
                if w_class in word_classes: # 'N','V','A','D','J','T','Y'
                    error1['Other'][w_class].add(label, pred)
                else:
                    error1['Other']['_'].add(label,pred)


        for k1, v1 in error1.items():
            if k1 == 'Other':
                total = 0
                found = 0
                for k2, v2 in v1.items():
                    total += v2.tp + v2.fn
                    found += v2.tp
                if total != 0:
                    r = found/total*100
                else:
                    r = 0
                print("Other: R: {:.1f} Count: {:d}".format(r,total))
            else:
                for k2, v2 in v1.items():
                    print(k1+k2+":  ", end='')
                    v2.print_eval()

class ErrorCount(object):
    def __init__(self):
        self.tp = 0
        self.tn = 0
        self.fp = 0 # This is always ZERO  since the labeler can't tell which type of error it is
        self.fn = 0

    def total(self):
        return self.tp+self.tn+self.fp+self.fn

    # Precision is always 0 or 1
    # because the labeler can't tell which type of error it is
    def precision(self):
        if self.tp == 0 and self.fp == 0:
            return 0
        else:
            return self.tp/(self.tp+self.fp)

    def recall(self):
        if self.tp == 0 and self.fn == 0:
            return 0
        else:
            return self.tp/(self.tp+self.fn)

    def f05(self):
        if self.precision()==0 or self.recall()==0:
            return 0
        else:
            return 1.25*(self.precision()*self.recall())/(0.25*self.precision()+self.recall())

    def add(self, label, pred):
        if label == 'i' and pred == 'i':
            self.tp += 1
        elif label == 'c' and pred == 'c':
            self.tn += 1
        elif label == 'c' and pred == 'i':
            self.fp += 1
        elif label == 'i' and pred == 'c':
            self.fn += 1

    def print_eval(self):
        # print(self.f05(), self.total())
        print("R: {:04.1f} Count: {:d}".format(
                self.recall()*100,
                self.total()
                ))
