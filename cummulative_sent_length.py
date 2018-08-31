#!/usr/bin/python3
'''
Plot the precision / recall against cummulative sentence lengths
i.e. precision and recall considering all sentences which are not longer than each sentence length (x-axis)

Args:
    gedout: path the the target .ged.tsv file
    plotname: the location and name of the png file
    threshold: the GED threshold
    max_length: (optional default = 150) 
        - only plot up to max_length
        - all sentences longer than this are put into max_length
    
Output:
    .png file in plotname.png
'''

import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import pdb

def main():
    if(len(sys.argv) < 4):
        print("Usage: python3 cummulative_sent_length.py gedout plotname threshold [max_length]")
        return

    gedout = sys.argv[1]
    plotname = sys.argv[2]
    threshold = float(sys.argv[3])


    if len(sys.argv) == 5:
        max_length = int(sys.argv[4])
    else:
        max_length = 150

    sent_range = list(range(1, max_length+1))
    # sentences[i] = {'c': 100, 'i': 120} at this threshold / sentence length = i
    sentences = {}
    for i in sent_range:
        sentences[i] = {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0}

    with open(gedout, 'r') as file:
        lines = file.readlines()

    count = 0       # count = count_c + count_i
    count_tp = 0
    count_fp = 0
    count_tn = 0
    count_fn = 0
    for line in lines:
        if line == '\n':
            if count == 0:
                pass
            elif count <= max_length:
                sentences[count]['tp'] += count_tp
                sentences[count]['fp'] += count_fp
                sentences[count]['tn'] += count_tn
                sentences[count]['fn'] += count_fn
            else:
                sentences[max_length]['tp'] += count_tp
                sentences[max_length]['fp'] += count_fp
                sentences[max_length]['tn'] += count_tn
                sentences[max_length]['fn'] += count_fn
            count = 0
            count_tp = 0
            count_fp = 0
            count_tn = 0
            count_fn = 0
            continue

        items = line.split()
        i_prob = float(items[-1].strip().strip('i:'))
        actual = items[2]

        if i_prob > threshold:
            if actual == 'i':
                count_tp += 1
            else:
                count_fp += 1
        else:
            if actual == 'c':
                count_tn += 1
            else:
                count_fn += 1

        count += 1

    cummulative_tp = 0
    cummulative_fp = 0
    cummulative_tn = 0
    cummulative_fn = 0

    for i in sent_range:
        cummulative_tp += sentences[i]['tp']
        cummulative_fp += sentences[i]['fp']
        cummulative_tn += sentences[i]['tn']
        cummulative_fn += sentences[i]['fn']
        try:
            sentences[i]['P'] = cummulative_tp / (cummulative_tp + cummulative_fp)
        except ZeroDivisionError:
            sentences[i]['P'] = 0

        try:
            sentences[i]['R'] = cummulative_tp / (cummulative_tp + cummulative_fn)
        except ZeroDivisionError:
            sentences[i]['R'] = 0


    precisions = [sentences[idx]['P'] for idx in sent_range]
    recalls = [sentences[idx]['R'] for idx in sent_range]

    # plottting using matplotlib
    plt.figure()
    plt.plot(sent_range, precisions, '.-', label="Precision")
    plt.plot(sent_range, recalls, '.-', label="Recall")


    plt.xlabel('Sent Length (cummulative up to)')
    plt.ylabel('P/R')
    plt.title("P/R of cummulative sentence lengths at threshold {}".format(threshold))
    plt.ylim([0.0, max(max(precisions),max(recalls))+0.05])
    plt.xlim([0, max_length])
    plt.legend()
    plt.savefig(plotname + '.png')





if __name__ == "__main__":
    main()
