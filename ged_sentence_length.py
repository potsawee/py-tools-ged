#!/usr/bin/python3
'''
Plot Histogram for Count against Sentence Length

Args:
    file: ged file - one word per line & use an empty line to separate sentences
    outpath: dir where the plot will be stored
    minlength: minimum sentence length
    maxlength: maximum sentence length

Output:
    .png saved at outpath/sentence-length-hist.png

'''

import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    if(len(sys.argv) != 5):
        print('Usage: python3 ged_sentence_length.py file outpath minlength maxlength')
        return

    file = sys.argv[1]
    outpath = sys.argv[2]
    minlength = int(sys.argv[3])
    maxlength = int(sys.argv[4])

    with open(file) as f:
        lines = f.readlines()

    sentence_legnths = []
    count = 0
    for line in lines:
        if line == "\n":
            if count < minlength:
                pass
            else:
                if count > maxlength:
                    sentence_legnths.append(maxlength)
                else:
                    sentence_legnths.append(count)
            count = 0
            continue
        else:
            count += 1

    bins = range(minlength, maxlength+1)
    plt.hist(sentence_legnths, bins,rwidth=1, alpha=0.8)
    plt.ylabel("Count")
    plt.xlabel("Sentence Length")
    plt.title(file)
    plt.savefig(outpath + "/sentence-length-hist.png")

    print("writing...", outpath + "/sentence-length-hist.png")


if __name__ == "__main__":
    main()
