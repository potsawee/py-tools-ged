'''
The CLC data is to be processed in the following ways:
[1] vanilla - Marek/Computer Lab
	(a) TLC - true lowercase e.g. ". the cat sat ."
	(b) Period-only-punctuation (individual "."s must only at either start/end)
	(c) TUC - Capitalise proper nouns e.g. england -> England, i -> I, first word
[2] baseline - no spelling mistakes
	(a) TLC - true lowercase e.g. ". the cat sat ."
	(b) Period-only-punctuation (individual "."s must only at either start/end)
	(c) TUC - Capitalise proper nouns e.g. england -> England, i -> I, first word
'''

import sys
import os
import string


def true_lowercase(input, output, start_tag='.', end_tag='.'):
    '''
    Step 1 of processing the CLC
        - to lowercase all the tokens
        - prepend & append a sentence with full-stops (or <s>, </s> ... optional)
        - never strip 'dot' e.g. I.B.M. (this issue will be handled later)
        - punctuations remain as they are
    '''

    with open(input, 'r') as f1:
        lines = f1.readlines()

    with open(output, 'w') as f2:

        sentence = [] # [('this', 'c'), ('is', 'c'), ...]

        for line in lines:

            if line == '\n': # end of sentence
                f2.write("{}\tc\n".format(start_tag))
                for word in sentence:
                    f2.write("{}\t{}\n".format(word[0], word[1]))
                f2.write("{}\tc\n".format(end_tag))
                f2.write("\n")
                sentence = []
                continue

            items = line.split()
            if(len(items) != 2):
                continue

            if(items[0] == '.'): # full stops at start/end added manually
                continue         # there should not be more full-stops

            token = items[0].lower()
            label = items[1]

            sentence.append((token,label))

def period_only(input,output):
    '''
    Step 2 of processing the CLC
        - remove all individual punctuations apart from '.'
    '''

    punc_set = set(string.punctuation)

    with open(input, 'r') as f1:
        lines = f1.readlines()


    with open(output, 'w') as f2:
        for line in lines:
            if line == '\n':
                f2.write(line)
                continue

            items = line.split()
            if(len(items) != 2):
                continue

            if items[0] in punc_set and items[0] != '.':
                continue

            f2.write(line)



def main():
    if (len(sys.argv) != 4):
        print("Usage: python3 clc_cued_processing.py option input output")
        return

    option = sys.argv[1]
    input = sys.argv[2]
    output = sys.argv[3]

    if(option == 'a'):
        # vanilla/baseline => truelowercase
        true_lowercase(input, output)

    if(option == 'b'):
        period_only(input, output)

    if(option == 'd1'):
        true_lowercase(input, output, '<s>', '</s>')

    print("processing done!")

if __name__ == "__main__":
    main()
