#!/usr/bin/python
'''
Plot PR-curve for all files (ged-output) in the specified folder
'''

import sys
import os
from gedoutparser import GedOutParser

def main():
    if(len(sys.argv) == 2):
        print("Usage: python3 posterior_probs_eval.py dir")
    parser = GedOutParser()

    ged_out_path = sys.argv[1]

    files = [os.path.join(ged_out_path, f) for f in os.listdir(ged_out_path) if (os.path.isfile(os.path.join(ged_out_path, f))) and '.tsv' in f]
    print(files)
    files.sort()
    scores_arr = []
    exp_path = os.path.dirname(ged_out_path)
    name_arr = [os.path.basename(f) for f in files]

    for i, file in enumerate(files):
        parser.read(file, name=file, skip_options=[1,2])

    parser.print_scores()
    parser.plot_pr_curves(savepath=exp_path+'/pr-curve-v2.png')


if __name__ == '__main__':
    print(__doc__)
    main()
