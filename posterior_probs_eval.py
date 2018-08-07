#!/usr/bin/python3
'''
Plot PR-curve for all files (ged-output) in the specified folder
'''

import sys
import os
from gedoutparser import GedOutParser

def main():
    if(len(sys.argv) != 2):
        print("Usage: python3 posterior_probs_eval.py dir")
        return


    ged_out_path = sys.argv[1]

    files = [os.path.join(ged_out_path, f) for f in os.listdir(ged_out_path) if (os.path.isfile(os.path.join(ged_out_path, f))) and '.tsv' in f]
    print(files)
    files.sort()
    scores_arr = []
    exp_path = os.path.dirname(ged_out_path)
    name_arr = [os.path.basename(f) for f in files]

    # ----------------------------------- #
    with open(files[0], 'r') as f:
        line0 = f.readlines()[0]
        num_columns = len(line0.split())
    if num_columns == 5: # DTAL/ASR
        parser = GedOutParser(columns=['token', 'error_type', 'label', 'c_prob', 'i_prob'])
    elif num_columns == 4: # CLC
        parser = GedOutParser(columns=['token', 'label', 'c_prob', 'i_prob'])
    # ----------------------------------- #

    for i, file in enumerate(files):
        name = os.path.basename(file)
        if num_columns == 5: #DTAL/ASR
            parser.read(file, name=name, skip_options=[1,3,4])
        else:
            parser.read(file, name=name, skip_options=[1])

    parser.print_scores()
    parser.plot_pr_curves(savepath=exp_path+'/pr-curve.png')


if __name__ == '__main__':
    print(__doc__)
    main()
