#!/usr/bin/python
'''
Process a DTAL transcription into inputs for GED
Original => DTAL transcription
File1 => Original & FP/IA/PW removed
File2 => File1 & Full-stop remove
File3 => File2 & RE removed
File4 => File3 & Capitalise first words
'''

import sys
from os import listdir
from os.path import isfile, join, exists
import pandas as pd
import datetime

def summary(df):
    summary_dict = dict()
    summary_dict['num_token'] = len(df)
    summary_dict['num_hesitation'] = len(df[df['token'] == '%hesitation%'])
    summary_dict['num_unclear'] = len(df[df['token'] == '%unclear%'])
    num_partial = 0
    for i in range(len(df)):
        if '%partial%' in df.loc[i]['token']:
            num_partial += 1
    summary_dict['num_partial'] = num_partial


    return summary_dict

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

def main():
    if(len(sys.argv) != 3):
        print('Usage: python3 dtal_processing.py tsv outpath')
        return

    tsv = sys.argv[1]
    outpath = sys.argv[2]


    if not exists(tsv):
        print('tsv path not exist')
        return

    file1 = open(outpath + '/ged-input/file1.tsv', 'w') #remove FP, IA, PW
    file2 = open(outpath + '/ged-input/file2.tsv', 'w') #remove Full-stops
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
            token = items[0]
            label = items[-1]

            error_type = items[1]

            # Ignore hesitation (FP) / unclear (IA) / partial (PW)
            if token == '%hesitation%' or token == '%unclear%':
                continue
            if '%partial%' in token:
                continue
            if '+' in token:
                token = token.replace('+','')
            # DTAL added '_' when a word is missing
            # it should not appear in the ASR output
            if token == '_':
                continue

            # in gedtoktsv - week4 there are tokens like . c _ etc
            if label != 'c' and label != 'i':
                continue

            # Ignore full-stops
            if token == '.':
                file1.write(line)
                continue

            file1.write(line)
            file2.write(line)

    file1.close()
    file2.close()

    # remove repetition file2 => file3
    file3 = outpath + '/ged-input/file3.tsv' #remove repetition
    remove_repeition(outpath + '/ged-input/file2.tsv', file3)



if __name__ == '__main__':
    main()
