"""
To decode the combine.txt file into one best output
using a language model to find the best sentence using the fluecy score
Support:
    - KenLM (source ~/anaconda3/bin/activate klm2)
"""

import sys
import kenlm
import math
import pdb

def decode(model, path):
    with open(path) as file:
        lines = file.readlines()

    # number of sentences
    S = int(lines[0].split()[-1])
    lines = lines[1:]

    lines = [line.strip() for line in lines]


    # for each sentence, there could be multiple candidates for correction
    idx = 0

    outputs = []

    for i in range(S):
        # number of candidates
        R = int(lines[idx].split()[-1])
        start = idx + 1
        end = start + R
        candidates = lines[start:end]

        one_best = find_one_best(model, candidates)
        # print(one_best)
        outputs.append(one_best)

        idx += (R+1)

    return outputs

def find_one_best(model, candidates):
    R = len(candidates)
    scores = [None] * R
    for i in range(R):
        n = len(candidates[i].split()) + 1 # for </s>
        scores[i] = model.score(candidates[i]) / n
    idx = scores.index(max(scores))
    return candidates[idx]


def main():
    if len(sys.argv) != 3:
        print("Usage: python2 decode.py file output")
        return

    path = sys.argv[1]
    output = sys.argv[2]

    # the language model (klm) is hard coded here!
    klm = "/home/alta/BLTSpeaking/ged-pm574/n-gram-lm/klm/models/ami8.5gram.klm"
    print("Loading:", klm)
    model = kenlm.LanguageModel(klm)
    print("Loaded:", klm)

    outputs = decode(model, path)
    with open(output, 'w') as file:
        for o in outputs:
            file.write(o + '\n')

if __name__ == "__main__":
    main()
