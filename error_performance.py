#!/usr/bin/python
'''
Print out error type performance of the GED system
Input:
    path to a ged output file
Output:
    None - print out the anlysis to terminal
'''

import sys
import pandas as pd
from collections import OrderedDict

class ErrorCount:
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

def main():
    if(len(sys.argv) != 2):
        print('Usage: python3 error_performace.py gedoutpath')
        return

    gedoutpath = sys.argv[1]
    print('----------------------------------------------------------')
    print('Error Type Performance: ged-out-path =', gedoutpath)
    print('----------------------------------------------------------')

    data = pd.read_csv(gedoutpath, delim_whitespace=True, header=None)
    data.columns = ['token', 'error_type' ,'label', 'c_prob', 'i_prob']
    preds= []
    for idx, row in data.iterrows():
        c_prob = float(row['c_prob'].strip('c:'))
        pred = 'c' if c_prob >= 0.5 else 'i'
        preds.append(pred)
    data['prediction'] = preds

    # ---- error type ---- #
    # refer to www.cl.cam.ac.uk/techreports/UCAM-CL-TR-915.pdf
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


if __name__ == '__main__':
    main()
