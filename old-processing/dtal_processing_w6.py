#!/usr/bin/python
'''
For processing DTAL transcription
'''

import sys
from os import listdir
from os.path import isfile, join, exists
import pandas as pd
import datetime
import string

def remove_errorneous_lines(input, output):
    '''

    '''

def remove_repetition(input, output):
    '''
    Can only be used after process_repetition already done!
    '''
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
            # label = items[-1].strip()
            # if label == 'i':
            #     pass
            # elif label == 'c':
            #     output_lines.pop()
            #     output_lines.append(line)
            pass
        prev_word = cur_word


    output_file = open(output, 'w')
    for line in output_lines:
        output_file.write(line)
    output_file.close()

def remove_hesitation(input, output):
    with open(input, 'r') as f1:
        lines = f1.readlines()
    with open(output, 'w') as f2:
        for line in lines:
            if line == '\n':
                f2.write(line)
                continue
            items = line.split()
            if(items[0] == '%hesitation%'):
                continue
            f2.write(line)

def process_repetition(input, output):
    '''
    Change the labels for repeated words
    [1] (c)-(i/RE) => (c)-(c/RE)
    [2] (i/RE)-(c) => (c/RE)-(c)
    [3] (i/...)-(i/RE) => (i/...)-(c/RE)
    '''
    with open(input, 'r') as f1:
        lines = f1.readlines()
    items = lines[0].split()
    output_lines = [(items[0], items[1], items[2])]
    prev_word = lines[0].split()[0]
    prev_err = lines[0].split()[1]
    prev_label = lines[0].split()[-1]
    for line in lines[1:]:
        if line == '\n':
            output_lines.append(('\n','_','_'))
            prev_word = ''
            continue

        items = line.split()
        cur_word = items[0]
        cur_err = items[1]
        cur_label = items[-1]
        if cur_word.lower() != prev_word.lower():
            output_lines.append((cur_word, cur_err, cur_label))
        else: # repetition found!
            if prev_label == 'c' and cur_label == 'c':
                output_lines.append((cur_word, cur_err, cur_label))
            elif prev_label == 'c' and cur_label == 'i':
                output_lines.append((cur_word, cur_err, 'c'))
            elif prev_label == 'i' and cur_label == 'c':
                output_lines.pop()
                output_lines.append((prev_word, prev_err, 'c'))
                output_lines.append((cur_word, cur_err, cur_label))
            elif prev_label == 'i' and cur_label == 'i':
                output_lines.pop()
                if prev_err == cur_err: #double repetition
                    output_lines.append((prev_word, prev_err, 'c'))
                    output_lines.append((cur_word, cur_err, 'c'))
                else:
                    output_lines.append((prev_word, prev_err, 'i'))
                    output_lines.append((cur_word, cur_err, 'c'))

        prev_word = cur_word
        prev_err = cur_err
        prev_label = cur_label

    with open(output, 'w') as f2:
        for line in output_lines:
            if line[0] == '\n':
                f2.write('\n')
            else:
                f2.write("{}\t{}\t{}\n".format(line[0], line[1], line[2]))

def process_unclear(input, output):
    with open(input, 'r') as f1:
        lines = f1.readlines()
    with open(output, 'w') as f2:
        for line in lines:
            if line == '\n':
                f2.write(line)
                continue
            items = line.split()
            if(items[0] == '%unclear%'):
                f2.write('%unclear%\t_\tc\n')
                continue
            f2.write(line)

def remove_false_start(input, output):
    with open(input, 'r') as f1:
        lines = f1.readlines()
    with open(output, 'w') as f2:
        for line in lines:
            if line == '\n':
                f2.write(line)
                continue
            items = line.split()
            if(items[1] == 'FS'):
                continue
            f2.write(line)

def true_lowercase(input, output, start_tag='.', end_tag='.'):
    # copied from clc_cued_processing
    with open(input, 'r') as f1:
        lines = f1.readlines()

    with open(output, 'w') as f2:

        sentence = [] # [('this', 'c'), ('is', 'c'), ...]

        for line in lines:

            if line == '\n': # end of sentence
                f2.write("{}\t_\tc\n".format(start_tag))
                for word in sentence:
                    f2.write("{}\t{}\t{}\n".format(word[0], word[1], word[2]))
                f2.write("{}\t_\tc\n".format(end_tag))
                f2.write("\n")
                sentence = []
                continue

            items = line.split()
            if(len(items) != 3):
                continue

            if(items[0] == '.'): # full stops at start/end added manually
                continue         # there should not be more full-stops

            token = items[0].lower()
            error_type = items[1]
            label = items[-1]
            sentence.append((token,error_type,label))

def period_only(input,output):
    # copied from clc_cued_processing

    punc_set = set(string.punctuation)

    with open(input, 'r') as f1:
        lines = f1.readlines()


    with open(output, 'w') as f2:
        for line in lines:
            if line == '\n':
                f2.write(line)
                continue

            items = line.split()
            if(len(items) != 3):
                continue

            if items[0] in punc_set and items[0] != '.':
                continue

            f2.write(line)

def basiccase(input, output):
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

def process_ASRI(input, output):
    with open(input, 'r') as f1:
        lines = f1.readlines()
    with open(output, 'w') as f2:
        for line in lines:
            if line == '\n':
                f2.write(line)
                continue
            items = line.split()
            if(items[1] == 'ASRI'):
                f2.write("{}\tASRI\tc\n".format(items[0]))
                continue
            f2.write(line)

def main():
    if(len(sys.argv) != 4):
        print('Usage: python3 dtal_processing_w6.py option input output')
        return

    option = sys.argv[1]
    input = sys.argv[2]
    output = sys.argv[3]

    if option == 'remove_hesitation':
        remove_hesitation(input, output)
    elif option == 'process_unclear':
        process_unclear(input, output)
    elif option == 'process_repetition':
        process_repetition(input, output)
    elif option == 'remove_repetition':
        remove_repetition(input, output)
    elif option == 'remove_false_start':
        remove_false_start(input, output)
    elif option == 'true_lowercase1':
        true_lowercase(input, output)
    elif option == 'true_lowercase2':
        true_lowercase(input, output, start_tag='<s>', end_tag='</s>')
    elif option == 'period_only':
        period_only(input, output)
    elif option == 'basiccase':
        basiccase(input, output)
    elif option == 'process_asri':
        process_ASRI(input, output)
    else:
        print('option invalid')
        return
    print('done!')



if __name__ == '__main__':
    # print(__doc__)
    main()
