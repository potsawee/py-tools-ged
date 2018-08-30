#!/usr/bin/python3
'''
Count how many lines in the target files have zero, one, two, ... field

Args:
    path: path to the target file

Output:
    print the output to the terminal e.g.
    linux> python3 assertdata.py clctraining-v3/dtal-exp-GEM4-1/output/4-REMOVE-DM-RE-FS.tsv

    zero:   3649
    one:    0
    two:    0
    three:  0
    four:   0
    five+:  69248

'''
import sys

def main():
    # path = '/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/tsv/ami1.train.ged.tsv'
    if len(sys.argv) != 2:
        print('Usage: python3 assertdata.py path')
        return

    path = sys.argv[1]

    zero = 0
    one = 0
    two = 0
    three = 0
    four = 0
    fivemore = 0
    with open(path) as file:
        for line in file:
            n = len(line.split())
            if n == 0:
                zero += 1
            elif n == 1:
                one += 1
            elif n == 2:
                two += 1
            elif n == 3:
                three += 1
            elif n == 4:
                four += 1
            else:
                fivemore += 1
    print("zero:  ", zero)
    print("one:   ", one)
    print("two:   ", two)
    print("three: ", three)
    print("four:  ", four)
    print("five+: ", fivemore)


if __name__ == "__main__":
    main()
