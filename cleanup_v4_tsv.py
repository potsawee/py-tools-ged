#!/usr/bin/python
'''
After using ./local/tools/mk_clctsvset.sh to obtain .tsv (version 4)
There are lines with this problem:
i
i.e. Just a label without any token
This script is for removing such lines

Usage give the folder containing v4 files that needs the processing
=> the script will output v4c files corresponding to the v4 files in the same folder

'''

import sys
from os import listdir, getcwd
from os.path import isfile, join

def cleanup_tsv(original, output):


    original_file = open(original, 'r')
    lines = original_file.read().splitlines()
    original_file.close()
    output_file = open(output, 'w')
    for line in lines:
        line_parts = line.split()
        if(len(line_parts) == 1):
            continue
        output_file.write(line + '\n')
    output_file.close()


def main():
    if (len(sys.argv) != 2):
        print('Usage: python3 cleanup_v4_tsv v4_tsv_dir')
        return
    mypath = sys.argv[1]
    # files = [join(mypath, f) for f in listdir(mypath) if (isfile(join(mypath, f)) and '.v4' in f)]
    files = [join(mypath, f) for f in listdir(mypath) if (isfile(join(mypath, f)) and '.spell' in f)]
    print('{} file(s) found'.format(len(files)))
    for file in files:
        original = file
        # output = file.replace('.original', '')
        # output = file.replace('v4', 'v4c')
        output = file.replace('.spell', '.spellc')
        cleanup_tsv(original, output)
    print('v4.tsv cleanup done!')


if __name__ == '__main__':
    main()
