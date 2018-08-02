#!/usr/bin/python

import sys
import os
import string

'''
Processing ged-tok-tsv files in the CLC
to re-train the sequence-labeler
    [1] remove punctuations ------------------------ (version6 / .ged.v6.tsv)
    [2] basic case (caplitalise first word & I) ---- (Version7 / .ged.v7.tsv)
Input:
    [1] original_path: the directory containing files to be processed
    [2] original_ext: the extension of the files
    [3] target_path: the directory to place the process files
    [4] target_ext: the extension of the processed files
Output:
    [1] the processed files with the specified extension
        in the target directory.
Usage:
    python3 clc_processing.py /home/alta/CLC/LNRC/exams/IELTS ged.spell.tsv
'''

def remove_punctuation(input, output):

    punc_set = set(string.punctuation)

    with open(input, 'r') as f1:
        lines = f1.readlines()

    errorneous_line = 0
    errorneous_line_idx = []
    with open(output, 'w') as f2:
        for idx, line in enumerate(lines):
            if line == '\n':
                f2.write(line)
                continue

            items = line.split()
            if(len(items) != 2):
                errorneous_line += 1
                errorneous_line_idx.append(idx)
                continue

            if items[0] in punc_set:
                continue

            f2.write(line)

def basic_case(input, output):
    '''
    [1] Capitalise first word in each sentence & I
        by detecting empty lines as sentence boundaries
    [2] To use basic case:
        Call main2
            e.g. python3 clc_processing.py mytsv.v6.tsv mytsv.v7.tsv

    '''
    with open(input, 'r') as f1:
        lines = f1.readlines()

    with open(output, 'w') as f2:

        begining = True
        for line in lines:
            if line == '\n':
                begining = True
                f2.write(line)
                continue

            line = line.lower()

            if not begining:
                items = line.split()
                if items[0] != 'i':
                    f2.write(line)
                else:
                    f2.write("{}\t{}\n".format('I', items[1]))

            else:
                items = line.split()
                token = items[0].capitalize()
                label = items[1]
                f2.write("{}\t{}\n".format(token, label))
                begining = False


def main2():
    input = sys.argv[1]
    output = sys.argv[2]
    basic_case(input, output)

def main3():
    input = sys.argv[1]
    output = sys.argv[2]
    remove_punctuation(input, output)


def main():
    if(len(sys.argv) != 5):
        print('Usage: python3 clc_processing.py original_path original_ext target_path target_ext')
        return
    original_path = sys.argv[1]
    original_ext = sys.argv[2]
    target_path = sys.argv[3]
    target_ext = sys.argv[4]

    orignal_files = [os.path.join(original_path, f) for f in os.listdir(original_path) \
            if (os.path.isfile(os.path.join(original_path, f))) and original_ext in f]

    new_files = [os.path.join(target_path, f) for f in os.listdir(original_path) \
            if (os.path.isfile(os.path.join(original_path, f))) and original_ext in f]

    new_files =[f.replace(original_ext, target_ext) for f in new_files]

    os.makedirs(target_path, exist_ok=True)

    for original, new in zip(orignal_files, new_files):
        remove_punctuation(original, new)

    print('clc_processing done!')

if __name__ == "__main__":
    # main()
    # main2()
    main3()
