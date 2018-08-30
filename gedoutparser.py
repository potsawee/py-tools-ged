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
'''
This class is implemented for reading/parsing the GED output file
'''
    def __init__(self, columns=['token', 'error_type', 'label', 'c_prob', 'i_prob']):
        self.columns = columns
        self.num_columns = len(columns)
        self.raw_data = []
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
        data = pd.read_csv(path, delim_whitespace=True, header=None, quoting=csv.QUOTE_NONE, na_filter=False)
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
        tokens = []
        for idx in range(len(data)):

            row = data.loc[idx]

            if 1 in skip_options: # do not score '.'
                if row['token'] == '.':
                    continue
            if 2 in skip_options: # do not score punctuation
                if row['token'] in punc_set:
                    continue
            if 3 in skip_options: # unclear
                if row['token'] == '%unclear%':
                    continue
            if 4 in skip_options: # partial
                if '%partial%' in row['token']:
                    continue
            if 5 in skip_options: # </s> tag
                if row['token'] == '</s>':
                    continue

            tokens.append(row['token'])
            i_prob = float(row['i_prob'].strip('i:'))
            i_probs.append(i_prob)
            labels.append(row['label'])

        raw_data = {'tokens': tokens, 'i_probs': i_probs, 'labels': labels}

        total = len(data)
        count = len(labels)
        error = 0
        for label in labels:
            if label == 'i':
                error += 1
        pr_dict = self.precision_recall(i_probs, labels)

        score = {'total': total,
                'count': count,
                'error': error,
                '%error': error/count,
                'P': pr_dict['P'],
                'R': pr_dict['R'],
                'F05': pr_dict['F05'],
                'precisions': pr_dict['precisions'],
                'recalls': pr_dict['recalls'],
                'threshold': pr_dict['threshold']}

        self.raw_data.append(raw_data)
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
            print('error:   {:d}'.format(score['error']))
            print('%error:  {:.1f}%'.format(score['%error']*100))
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

    def probs_diff(self, idx1, idx2, max_num=20):
        if(self.scores[idx1]['count'] != self.scores[idx2]['count']):
            print('two files do not have the same counts, {} != {}'.format(
                    self.scores[idx1]['count'],
                    self.scores[idx2]['count']))
            return
        count = self.scores[idx1]['count']
        diff = []
        for idx in range(count):
            token1 = self.raw_data[idx1]['tokens'][idx]
            label1 = self.raw_data[idx1]['labels'][idx]
            i1 = self.raw_data[idx1]['i_probs'][idx]

            token2 = self.raw_data[idx2]['tokens'][idx]
            label2 = self.raw_data[idx2]['labels'][idx]
            i2 = self.raw_data[idx2]['i_probs'][idx]

            if token1.lower() != token2.lower():
                print('Index {}: {} != {}'.format(idx, token1, token2))
                return

            diff.append(np.abs(i1-i2))

        diff = np.array(diff)
        diff_idx = np.argsort(diff)[::-1]
        print("{:15}     Index   Label   Diff   i1     i2".format("Word"))
        print("----------------------------------------------------------")
        for j, idx in enumerate(diff_idx):
            print("{:15}   {:>7d}   {:5}   {:.3f}  {:.3f}  {:.3f}".format(
                    self.raw_data[idx1]['tokens'][idx],
                    idx,
                    self.raw_data[idx1]['labels'][idx],
                    diff[idx],
                    self.raw_data[idx1]['i_probs'][idx],
                    self.raw_data[idx2]['i_probs'][idx]))
            if j>=max_num:
                break

    def x_models(self, idx1, idx2, savepath=None):
        if(self.scores[idx1]['count'] != self.scores[idx2]['count']):
            print('two files do not have the same counts, {} != {}'.format(
                    self.scores[idx1]['count'],
                    self.scores[idx2]['count']))
            return
        count = self.scores[idx1]['count']
        i_arr1 = self.raw_data[idx1]['i_probs']
        i_arr2 = self.raw_data[idx2]['i_probs']
        labels = self.raw_data[idx1]['labels']

        errors1 = []
        errors2 = []
        errors_total = []

        thresholds = np.linspace(0.05,1.0,20) # 0.05, 0.10, ..., 0.95, 1.00
        for threshold in thresholds:
            error1 = 0
            error2 = 0
            for j in range(count):
                # there are four cases: (1) c-c (2) c-i (3) i-c (4) i-i
                # but we are only interested in c-i and i-c i.e. when the two systems are different
                # at a particular threshold => we want %of (#2+#3) / (#1+#2+#3#4)
                if(i_arr1[j] < threshold and i_arr2[j] > threshold):
                    error1 += 1
                elif(i_arr1[j] > threshold and i_arr2[j] < threshold):
                    error2 += 1
            errors1.append(error1)
            errors2.append(error2)
            errors_total.append(error1 + error2)

        errors1 = [e*100/count for e in errors1]
        errors2 = [e*100/count for e in errors2]
        errors_total = [e*100/count for e in errors_total]


        plt.figure()
        plt.plot(thresholds, errors2, '.-', label='sys1 = i & sys2 = c')
        plt.plot(thresholds, errors1, '.-', label='sys1 = c & sys2 = i')
        plt.plot(thresholds, errors_total, '.-', label='c-i OR i-c')

        # Operating Point
        # err_confidence1 = self.scores[idx1]['threshold']
        # err1 = errors1[thresholds.tolist().index(err_confidence1)]
        # err_confidence2 = self.scores[idx2]['threshold']
        # err2 = errors2[thresholds.tolist().index(err_confidence2)]
        # plt.plot((0, err_confidence1), (err1, err1), '-', color = '0.5')
        # plt.plot((err_confidence1, err_confidence1), (0, err1), '-', color = '0.5')
        # plt.plot((0, err_confidence2), (err2, err2), '-', color = '0.5')
        # plt.plot((err_confidence2, err_confidence2), (0, err2), '-', color = '0.5')

        plt.xlabel('Error Confidence')
        plt.ylabel('Percent errors')
        plt.title("System 1 vs System 2")
        # plt.ylim([0.0, 1.0])
        plt.xlim([0.0, 1.0])
        plt.legend()

        if savepath == None:
            plt.show()
        else:
            plt.savefig(savepath)

    def histogram(self, indices, bin_num=100, savepath=None):
        histogram = plt.figure()

        bins = np.linspace(0, 1, bin_num)
        for i in indices:
            plt.hist(self.raw_data[i]['i_probs'], bins, alpha=0.5, label=self.names[i])

        plt.xlabel('Probabilities (i_prob)')
        plt.ylabel('Count')
        # plt.xlim([0.5, 1.0])
        # plt.ylim([0.0, 100])
        plt.yscale('log', nonposy='clip')
        plt.title("Histogram")
        plt.legend()

        if savepath == None:
            plt.show()
        else:
            plt.savefig(savepath)


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
