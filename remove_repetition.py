#!/usr/bin/python
'''
Remove repeition tokens from a GED tsv file
Usage: python3 remove_repeition.py input output
'''

import sys
from os import listdir
from os.path import isfile, join
from pathlib import Path
import pandas as pd

def main():
    if(len(sys.argv) != 3):
        print('Usage: python3 remove_repeition.py input output')
        return
    input = sys.argv[1]
    output = sys.argv[2]

    input_file = Path(input)
    if not input_file.is_file():
        print('input file not exist')
        return

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

    print('Remove Repeition Done!')


if __name__ == '__main__':
    main()
