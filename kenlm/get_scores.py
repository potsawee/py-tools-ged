import sys
import kenlm
import math
import pdb

"""
Use python2 e.g. conda activate klm2
no <s> </s> are required in the input file
"""

def main():
    if len(sys.argv) != 4:
        print("usage: python2 get_score.py klm file option")
        return

    klm = sys.argv[1]
    path = sys.argv[2]
    option = sys.argv[3] # 1 = score | 2 = #OOV

    with open(path) as file:
        lines = file.readlines()

    # lines = [line.strip() for line in lines]
    lines = [line.strip('.').strip().lower() for line in lines]

    model = kenlm.LanguageModel(klm)

    # model.score computes
    # log10 p(sentence </s> | <s>)
    ln10 = math.log(10) # math.log is base e

    if option == '1':
        for line in lines:
            n = len(line.split()) + 1 # for </s>
            score = model.score(line) * ln10 / n
            print(score)

    elif option == '2':
        for line in lines:
            oov_count = 0
            words = line.split()
            for word in words:
                if word not in model:
                    oov_count +=1
            print(oov_count)


if __name__ == '__main__':
    main()
