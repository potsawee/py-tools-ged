#!/usr/bin/python3
"""
Find the percentage of any words being incorrect in a given .ged.tsv file - P(word == 'i')
    
    File Format - First Field == word / Last Field == label e.g.:
    she     c
    like    i
    cats    c
    
Args:
    filepath: path the the target .ged.tsv file
    min_count: (optional default = 20) only print words appearing more than min_count
    
Output:
    the result will be printed out to the terminal e.g.
    linux> python3 find_i.py /home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/ami-work/ami6.ged.tsv
    
    Word           : %Incor: Count
    ----------------------------------------------------------
    <DEL>          : 1.000:  1205
    definitly      : 1.000:    32
    differents     : 1.000:    38
    basicaly       : 1.000:    21
    occured        : 1.000:    23
    *emp           : 1.000:    23
    cording        : 1.000:    52
    
"""

import sys
import operator

def main():
    if(len(sys.argv) < 2):
        print('Usage: python3 find_i.py filepath [min_count]')
        return

    path = sys.argv[1]
    if len(sys.argv) == 3:
        min_count = int(sys.argv[2])
    else:
        min_count = 20

    # path = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/ami6+cts6+fisher6.ged.tsv"
    # path = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/ami-work/ami6.ged.tsv"
    # path = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/work-24082018/master.gedx.ins.tsv"

    words_dict = {}

    with open(path) as file:
        for line in file:
            if line == '\n':
                continue
            items = line.split()
            word = items[0]
            label = items[-1].strip()

            if word not in words_dict:
                words_dict[word] = {'c': 0, 'i': 0}
                words_dict[word][label] += 1
            else:
                words_dict[word][label] += 1

    for word, value in words_dict.items():
        words_dict[word]['err'] = value['i'] / ( value['c'] + value['i'] )
        words_dict[word]['count'] = value['c'] + value['i']

    words_list = {}
    for word, value in words_dict.items():
        if value['c'] + value['i'] < min_count:
            continue
        words_list[word] = value['err']

    sorted_words_list = reversed(sorted(words_list.items(), key=operator.itemgetter(1)))

    counter = 0
    print("{:15}: {:.6}: {:5}".format("Word","%Incorrect","Count"))
    print("----------------------------------------------------------")
    for items in sorted_words_list:
        word = items[0]
        err = items[1]
        print("{:15}: {:.3f}: {:5d}".format(word,err,words_dict[word]['count']))
        counter += 1
        # if counter % 100 == 0:
            # input("continue?")


if __name__ == '__main__':
    main()
