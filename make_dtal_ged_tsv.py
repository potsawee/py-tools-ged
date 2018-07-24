#!/usr/bin/python
'''
Create a GED input file from tsv files
Please specify the post-processing steps required in this script
'''

import sys
from os import listdir
from os.path import isfile, join, exists
import pandas as pd

def main():
    if(len(sys.argv) != 3):
        print('Usage: python3 make_dtal_ged_tsv.py tsv_dir ged_input_file')
        return
    tsv_dir = sys.argv[1]
    ged_input_file = sys.argv[2]

    if not exists(tsv_dir):
        print('tsv path not exist')
        return

    tsv_files = [join(tsv_dir, f) for f in listdir(tsv_dir) if (isfile(join(tsv_dir, f)) and '.tsv' in f)]
    tsv_files.sort()
    file = open(ged_input_file, 'w')
    for tsv in tsv_files:
        df = pd.read_csv(tsv, delim_whitespace=True)
        for idx, row in df.iterrows():
            token = row['token']

            #--------- Post-processing ---------#
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
            # token = token.lower()
            # if token == '.':
            #     continue
            if token == 'i':
                token = 'I'
            #-----------------------------------#

            label = 'c' if row['grammError'] == 'O' else 'i'
            if row['grammError'] == 'O':
                err_type = 'NaN'
            elif row['grammError'] == 'I':

            # --------------------------------------------------------------- #
            # grammError == 'I' means the error is the same as the previous one
            # this has been corrected since exp2
                while(df.iloc[idx]['grammError'] == 'I'):
                    idx -= 1
                err_type = df.iloc[idx]['grammErrorType']
            # --------------------------------------------------------------- #

            else:
                err_type = row['grammErrorType']
            s = token + '\t' + err_type + '\t' + label  + '\n'

            file.write(s)

            if token == '.':
                file.write('\n')

        # file.write('\n')

    file.close()
    print('Processing Done!')


if __name__ == '__main__':
    main()
