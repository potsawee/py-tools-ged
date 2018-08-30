#!/usr/bin/python3
'''
Plot PR-curve for all files (ged-output) in the specified directory

Args:
    dir: Directory where the output of the GED system are located - only looks for .tsv files
    skip_options: if specified it will not score e.g. </s> - but by default this should not needed. 
                  See gedoutparser.py for more detail about skip_options
    
Return:
    1. Print out - Total, Count, Error, %Error, and Precision/Recall/F0.5 
    (at the operating point - highest F0.5) to the terminal for all .tsv files in the specified directory
    2. Save the PR-curve in the same directory - /pr-curve.png
'''

import sys
import os
from gedoutparser import GedOutParser

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 posterior_probs_eval.py dir [skip_options]")
        return
    # print(__doc__)

    ged_out_path = sys.argv[1]

    # if this argument exists do not skip any word!
    # if len(sys.argv) == 3:
    #     skip_options = False
    # else:
    #     skip_options = True
    if len(sys.argv) > 2:
        skip_options = []
        for i in range(len(sys.argv)-2):
            skip_options.append(int(sys.argv[i+2]))
    else:
        skip_options = None

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
    elif num_columns == 4: # CLC (before ged.spell.v3)
        parser = GedOutParser(columns=['token', 'label', 'c_prob', 'i_prob'])
    # ----------------------------------- #

    for i, file in enumerate(files):
        name = os.path.basename(file).split(".")[0]
        if skip_options != None:
            parser.read(file, name=name, skip_options=skip_options)
        else:
            if num_columns == 5: #DTAL/ASR
                # parser.read(file, name=name, skip_options=[1,3,4])
                parser.read(file, name=name, skip_options=[3,4,5])
            else: # old CLC format
                # parser.read(file, name=name, skip_options=[1])
                parser.read(file, name=name, skip_options=[5])

    parser.print_scores()
    parser.plot_pr_curves(savepath=exp_path+'/pr-curve.png')


if __name__ == '__main__':
    main()
