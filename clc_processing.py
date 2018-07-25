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
    [1] path: the directory containing files to be processed
    [2] original_ext: the extension of the files
    [3] target_ext: the extension of the processed files
Output:
    [1] the processed files with the specified extension
        in the same directory.
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


def main():
    if(len(sys.argv) != 4):
        print('Usage: python3 clc_processing.py path original_ext target_ext')
        return
    path = sys.argv[1]
    original_ext = sys.argv[2]
    target_ext = sys.argv[3]

    orignal_files = [os.path.join(path, f) for f in os.listdir(path) \
            if (os.path.isfile(os.path.join(path, f))) and original_ext in f]

    new_files =[f.replace(original_ext, target_ext) for f in orignal_files]

    for original, new in zip(orignal_files, new_files):
        remove_punctuation(original, new)

    print('clc_processing done!')

if __name__ == "__main__":
    main()
