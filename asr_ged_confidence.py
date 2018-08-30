#!/usr/bin/python3
'''
Plot PR curves at different ASR confidence thresholds

Args:
    gedout: Target file (the GED output)

Return:
    Save the plot in the same directory - /asr-pr-conf.png
'''

import sys
import os
import numpy as np
import pandas as pd
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def readin(gedout, skip_options):
    columns=['token', 'error_type', 'confidence', 'label', 'c_prob', 'i_prob']
    data = pd.read_csv(gedout, delim_whitespace=True, header=None, quoting=csv.QUOTE_NONE, na_filter=False)
    data.columns = columns

    i_probs = []
    labels = []
    tokens = []
    confidences = []
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
        i_probs.append(float(row['i_prob'].strip('i:')))
        labels.append(row['label'])
        confidences.append(float(row['confidence']))

    raw_data = {'tokens': tokens, 'i_probs': i_probs, 'labels': labels, 'confidences': confidences}
    return raw_data

def precision_recall_asrconf(i_probs, labels, confidences, asr_threshold):
    precisions = []
    recalls = []
    f05_scores = []
    thresholds = np.linspace(0,0.95,20)
    for threshold in thresholds:
        true_pos = 0
        true_neg = 0
        false_pos = 0
        false_neg = 0
        for i_prob, label, conf in zip(i_probs, labels, confidences):
            if(i_prob > threshold and conf > asr_threshold):
                if(label == 'i'):
                    true_pos += 1
                else: # correct
                    false_pos += 1
            else: # i_prob < threshold or conf < asr_threshold
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
def main():
    if(len(sys.argv) != 2):
        print('Usage: python3 asr_ged_confidence.py gedout')
        return

    gedout = sys.argv[1]
    # output = sys.argv[2]

    raw_data = readin(gedout, skip_options=[3,4,5])
    i_probs = raw_data['i_probs']
    labels = raw_data['labels']
    confidences = raw_data['confidences']

    asr_thresholds = [0.0, 0.2, 0.4, 0.6, 0.8]
    precision_recalls = []
    for asr_threshold in asr_thresholds:
        precision_recall = precision_recall_asrconf(i_probs, labels, confidences, asr_threshold)
        precision_recalls.append(precision_recall)

    plt.figure()
    for asr_threshold, precision_recall in zip(asr_thresholds, precision_recalls):
        plt.plot(precision_recall['recalls'], precision_recall['precisions'],
                '.-', label='ASR Threshold='+str(asr_threshold))

    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title("Precision-Recall curve")
    plt.ylim([0.0, 1.0])
    plt.xlim([0.0, 1.0])
    plt.legend()

    savepath = os.path.dirname(gedout) + '/asr-pr-conf.png'
    plt.savefig(savepath)

    print("plotting done...", savepath)


if __name__ == "__main__":
    main()
