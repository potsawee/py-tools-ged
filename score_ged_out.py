#!/usr/bin/python
'''
Print Precision, Recall, F1-score, F0.5-score of a GED output file
Show a ROC curve and a precision-recall curve
'''

import sys
import os
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import precision_recall_curve, roc_curve, auc, average_precision_score

def get_scores(ged_output_path, count_dict=None):
    data = pd.read_csv(ged_output_path, delim_whitespace=True, header=None)
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
    for idx, row in data.iterrows():
        c_prob = float(row['c_prob'].strip('c:'))
        i_prob.append(1-c_prob)
        predict = 'c' if c_prob >= 0.5 else 'i'
        actual = row['label']
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

    assert len(data) == true_positive + true_negative + false_positive + false_negative

    total = len(data)
    p = true_positive / (true_positive+false_positive)
    r = true_positive / (true_positive+false_negative)
    if p != 0 or r != 0:
        f1 = 2 * (p*r)/(p+r)
        f05 = 1.25 * (p*r)/(0.25*p + r)
    else:
        f1 = 0
        f05 = 0
    accuracy = (true_positive+true_negative)/total

    scores = {'total': total,
             'p': p, 'r': r,
             'f1': f1, 'f05': f05,
             'accuracy': accuracy,
             'i_prob': i_prob,
             'binary_label': [data['label'] == 'i']}
    return scores


def print_scores(scores):

    print('----------------------------------------------------------')
    print('Total Token: {:d}'.format(scores['total']))
    print('Precision:   {:.1f}%'.format(scores['p']*100))
    print('Recall:      {:.1f}%'.format(scores['r']*100))
    print('F1 score:    {:.1f}%'.format(scores['f1']*100))
    print('F0.5 score:  {:.1f}%'.format(scores['f05']*100))
    print('Accuracy:    {:.1f}%'.format(scores['accuracy']*100))
#     print('----------------------------------------------------------')

def plot_roc_curve(scores):
    preds = scores['i_prob']
    binary_label = scores['binary_label']
    test_label = []
    for b in binary_label[0]:
        if b == True:
            test_label.append(1)
        else:
            test_label.append(0)


    fpr, tpr, threshold = roc_curve(test_label, preds)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.title('Receiver Operating Characteristic')
    #plt.grid()
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.3f' % roc_auc)
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()


def plot_precision_reall_curve(scores, name, f05=True):

    preds = scores['i_prob']
    binary_label = scores['binary_label']
    test_label = []
    for b in binary_label[0]:
        if b == True:
            test_label.append(1)
        else:
            test_label.append(0)

    # precision, recall, _ = precision_recall_curve(test_label, preds)
    # average_precision = average_precision_score(test_label, preds)
    # plt.figure()
    # plt.step(recall, precision, color='b', alpha=0.2, where='post')
    # plt.fill_between(recall, precision, step='post', alpha=0.2, color='b')
    precisions = []
    recalls = []
    f05 = []

    for threshold in np.linspace(0,1.0,11):
        true_pos = 0
        true_neg = 0
        false_pos = 0
        false_neg = 0
        for pred, incorrect in zip(preds, binary_label[0]):
            if(pred > threshold):
                if(incorrect):
                    true_pos += 1
                else: # correct
                    false_pos += 1
            else: # pred < threshold
                if(incorrect):
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
        try:
            f05.append(1.25 * (precision*recall)/(0.25*precision + recall))
        except ZeroDivisionError:
            f05.append(0)
    if(f05):
        for label, x, y in zip(f05[:-1], recalls[:-1], precisions[:-1]):
            # the last element is not plotted as it corresponds to p=0, r=0 => not predicting anything!
            plt.annotate("{:.1f}".format(label*100), xy=(x, y),
                        xytext=(10, 10), textcoords='offset points',
                        ha='right', va='bottom')
        plt.title("Precision-Recall curve with F0.5 annotated at each point")
    else:
        plt.title("Precision-Recall curve")
    plt.plot(recalls, precisions, 'o-')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    # plt.title('Precision-Recall curve: AP={0:0.3f}'.format(average_precision))
    plt.show()
#     plt.savefig(name + '.png')

def main():
    if(len(sys.argv) != 2):
        print('Usage: python3 score_ged_out.py ged_out_file')
        return

    file_path = sys.argv[1]
    my_file = Path(file_path)
    name = os.path.basename(file_path)
    if not my_file.is_file():
        print(file_path + ': not exist')
        return

    scores = get_scores(file_path)
    print('----------------------------------------------------------')
    print(file_path)
    print_scores(scores)

#     plot_precision_reall_curve(scores,name)
    # plot_roc_curve(scores)


if __name__ == '__main__':
    main()
