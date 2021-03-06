#!/usr/bin/python3
'''
Find False Positives above the threshold in the target file

Args:
    file: Target file (the GED output)
    threshold: i_prob threshold above which word is predicted as incorrect

Return:
    print out a list of the the false positives to the terminal
    linux> python3 false-positive.py clctraining-v3/dtal-exp-GEM4-1/output/4-REMOVE-DM-RE-FS.tsv 0.9

    ---------------------------------------
    File: posterior/version7-2-combine/combine-1and3.tsv
    ---------------------------------------
    threshold: 0.9
    false postive count: 6
    precision = 89.1 | recall = 0.5
    ---------------------------------------
    ---------------------------------------

    what    _       c       c:0.97920746    i:0.020792535
    do      _       c       c:0.95429325    i:0.0457068
    you     _       c       c:0.98381084    i:0.016189173
    mean    _       c       c:0.9720767     i:0.027923247
    by      _       c       c:0.87792575    i:0.122074224
    ### traveling   _       c       c:0.008663192   i:0.9913368
    first   _       c       c:0.500374      i:0.49962598
    class   _       c       c:0.9149868     i:0.08501321
    </s>    _       c       c:0.9999894     i:1.0577641e-05

    </s>    _       c       c:0.9999906     i:9.360367e-06


'''

import sys

def main():
    if(len(sys.argv) != 3):
        print('Usage: python3 false-positive.py file threshold')
        return

    file = sys.argv[1]
    threshold = float(sys.argv[2])

    with open(file) as f:
        lines = f.readlines()

    fp_list = []
    true_pos = 0
    true_neg = 0
    false_pos = 0
    false_neg = 0
    for i, line in enumerate(lines):
        if line == "\n":
            continue

        items = line.split()
        word = items[0]
        error_type = items[1]
        label = items[-3]
        i_prob = float(items[-1].strip('i:'))

        if word == "%unclear%" or "%partial%" in word or word == "</s>":
            continue

        if i_prob > threshold and label == 'c':
            fp_list.append(i)

        if i_prob > threshold:
            if label == 'i':
                true_pos += 1
            else:
                false_pos += 1
        else:
            if label == 'i':
                false_neg += 1
            else:
                true_neg += 1

    precision = true_pos / (true_pos + false_pos)
    recall = true_pos / (true_pos + false_neg)
    f05 = 1.25 * (precision*recall)/(0.25*precision + recall)

    print("---------------------------------------")
    print("File:", file)
    print("---------------------------------------")
    print("threshold:",threshold)
    print("false postive count:",len(fp_list))
    print("precision = {:.1f}% | recall = {:.1f}% | f0.5 = {:.1f}%".format(precision*100, recall*100, f05*100))
    print("---------------------------------------")

    for i in fp_list:
        # print("\n")
        try:
            print("---------------------------------------\n")
            print("{}{}{}{}{}### {}{}{}{}{}{}\n".format(
                lines[i-5],
                lines[i-4],
                lines[i-3],
                lines[i-2],
                lines[i-1],
                lines[i],
                lines[i+1],
                lines[i+2],
                lines[i+3],
                lines[i+4],
                lines[i+5]
            ))
        except IndexError:
            pass



if __name__ == "__main__":
    main()
