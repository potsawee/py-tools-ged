#!/usr/bin/python

'''
To parse .ctm.sgml file to tsv with confidence and error type
'''

import sys
from bs4 import BeautifulSoup

def main():
    if(len(sys.argv) != 3):
        print('Usage: python3 asr_xml_parser_to_tsv.py sgml tsv')
        return

    sgml = sys.argv[1]
    tsv = sys.argv[2]

    infile = open(sgml, 'r')
    outfile = open(tsv, 'w')
    text = infile.read()
    infile.close()
    markup = BeautifulSoup(text, "html5lib")
    paths = markup.findAll('path')

    # Each path is roughly to a sentence
    for path in paths:
        words = path.get_text().strip().split(':')
        idx = 0
        while idx < (len(words)):
            items = words[idx].split(',')
            # skip the deletion problem and treat the next token to be incorrect
            if items[0] == 'C':
                label = 'c'
                error = 'NaN'
            elif items[0] == 'D':
                idx += 1
                label = 'i'
                error = 'D'
                items = words[idx].split(',')
            else: # 'S', 'I'
                label = 'i'
                error = items[0]

            token = items[2].strip('"')
            confidence = items[4]

            # post-processing e.g. removing '.', lowercasing etc.
            if token == 'i':
                token = 'I'

            if token != '' and token != '.':
                outfile.write('\t'.join([token, confidence, error, label]) + '\n')
            idx += 1
        outfile.write('\n')

    outfile.close()

    print('Parsing done!')


if __name__ == '__main__':
    main()
