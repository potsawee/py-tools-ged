#!/usr/bin/python
'''
Process a CUED-ASR transcription into inputs for GED
* original_file => CUED-ASR transcription
* ged-input/
    file1 => no punctuation & same case
    file2 => file1 & strip FP/IA/PW
    file3 => file2 & remove RE
    file4 => file3 & basic case (first letter & 'I')
'''

import sys
from os import listdir
from os.path import isfile, join, exists
import pandas as pd
import datetime


def remove_repeition(input, output):
    input_file = open(input, 'r')
    input_lines = input_file.readlines()
    input_file.close()
    output_lines = [input_lines[0]]
    prev_word = input_lines[0].split('\t')[0]
    for line in input_lines[1:]:
        if line == '\n':
            output_lines.append(line)
            prev_word = ''
            continue

        items = line.split('\t')
        cur_word = items[0]
        if cur_word != prev_word:
            output_lines.append(line)
        else: # repetition found!
            label = items[-1].strip()
            if label == 'i':
                pass
            elif label == 'c':
                output_lines.pop()
                output_lines.append(line)
        prev_word = cur_word


    output_file = open(output, 'w')
    for line in output_lines:
        output_file.write(line)
    output_file.close()

def capitalise(input, output):
    with open(input, 'r') as input_file:
        input_lines = input_file.readlines()
    output_file = open(output, 'w')

    begining = True
    for line in input_lines:
        if line == '\n':
            begining = True
            output_file.write(line)
            continue

        if not begining:
            items = line.split('\t')
            if items[0] != 'i':
                output_file.write(line)
            else: # 'i' => 'I'
                token = 'I'
                error_type = items[1]
                label = items[-1]
                output_file.write('\t'.join([token, error_type, label]))
        else:
            items = line.split('\t')
            token = items[0].capitalize()
            error_type = items[1]
            label = items[-1]
            output_file.write('\t'.join([token, error_type, label]))
            begining = False

    output_file.close()

def main():
    if(len(sys.argv) != 3):
        print('Usage: python3 asr_processing.py tsv outpath')
        return

    tsv = sys.argv[1]
    outpath = sys.argv[2]


    if not exists(tsv):
        print('tsv path not exist')
        return

    file1 = open(outpath + '/ged-input/file1.tsv', 'w') # no punctuation & same case
    file2 = open(outpath + '/ged-input/file2.tsv', 'w') # remove FP/IA/PW
    with open(tsv, 'r') as tsv_file:
        lines = tsv_file.readlines()
        for line in lines:
            # empty line
            if line == '\n':
                file1.write(line)
                file2.write(line)
                continue
            items = line.split()
            if(len(items) < 2):
                continue

            token = items[0].lower()
            label = items[-1].strip()
            error_type = items[1]

            line = '\t'.join([token, error_type, label])
            line += '\n'

            # in gedtoktsv - week4 there are tokens like . c _ etc
            if label != 'c' and label != 'i':
                continue
            # Ignore punctuations
            if token in ['.', '!', ',', '(', ')']:
                continue

            # Ignore hesitation (FP) / unclear (IA) / partial (PW)
            if token == '%hesitation%' or token == '%unclear%':
                file1.write(line)
                continue
            if '%partial%' in token:
                file1.write(line)
                continue

            file1.write(line)
            file2.write(line)
    file1.close()
    file2.close()

    # remove repetition file2 => file3
    file3 = outpath + '/ged-input/file3.tsv' #remove repetition
    remove_repeition(outpath + '/ged-input/file2.tsv', file3)

    # capitalise first words file3 => file4
    file4 = outpath + '/ged-input/file4.tsv'
    capitalise(file3, file4)



if __name__ == '__main__':
    print(__doc__)
    main()
