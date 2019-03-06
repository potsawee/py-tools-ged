"""
hyp1: the cat sits in the mat
hyp2: the cat sat on mat

confusion set:

<s> --- the --- cat --- sits --- in --- the --- mat --- </s>
                     -- sat ---- ** --- on ----

"""

import sys
import pdb
repo = '/home/alta/BLTSpeaking/exp-ytl28/local-ytl/py-tools/'
sys.path.insert(0, repo)
import rdlextra_bias2right as rdlextra

def align_corpus(cor1, cor2):
    with open(cor1, 'r') as file:
        lines1 = file.readlines()
    with open(cor2, 'r') as file:
        lines2 = file.readlines()

    if len(lines1) != len(lines2):
        raise Exception("sentence lengths not match")

    print("#! S = {}".format(len(lines1))) # number of sentences

    for sent1, sent2 in zip(lines1, lines2):
        align_sentence_charlevel(sent1.strip(), sent2.strip())
        # print()

def align_sentence_charlevel(sent1, sent2):
    a = sent1.split()
    b = sent2.split()

    if len(a) == 0 and len(b) == 0:
        return

    al = list(rdlextra.WagnerFischer(a, b).alignments())[0]

    a_idx = 0
    b_idx = 0
    alis = []
    blis = []
    for j in range(len(al)):
        if al[j] == 'D':
            curr_a = a[a_idx]
            curr_b = '*' * len(curr_a)
            a_idx += 1
        elif al[j] == 'I':
            curr_b = b[b_idx]
            curr_a = '*' * len(curr_b)
            b_idx += 1
        else:
            curr_a = a[a_idx]
            curr_b = b[b_idx]
            a_idx += 1
            b_idx += 1
        alis.append(curr_a)
        blis.append(curr_b)

    # for a1, b1 in zip(alis, blis):
    #     label = 'c' if a1 == b1 else 'i'
    #     print('{}\t{}\t{}'.format(a1,b1,label))
    table, R = build_table(alis, blis)
    print("#! R = {}".format(R))
    for row in table:
        row = [x for x in row if '*' not in x]
        sentence = " ".join(row)
        print("{}".format(sentence))

def build_table(alis, blis):
    ifbranchs = []
    if len(alis) != len(blis):
        raise Exception("len(alis) != len(blis)")

    T = len(alis) # number of timesteps
    N = 0 # number of branches

    for a, b in zip(alis, blis):
        if a == b:
            ifbranchs.append(False)
        else:
            ifbranchs.append(True)
            N += 1

    R = 2 ** N # number of rows in the table
    branch = 0

    table = []
    for r in range(R):
        table.append([None] * T)
    # pdb.set_trace()

    for t in range(T):
        if not ifbranchs[t]:
            for r in range(R):
                table[r][t] = alis[t]
        else:
            branch += 1
            split = int(R / 2 ** branch)
            current = alis[t]
            for r in range(R):
                table[r][t] = current
                if (r+1) % split == 0:
                    if current == alis[t]:
                        current = blis[t]
                    elif current == blis[t]:
                        current = alis[t]
                    else:
                        raise Exception("unexpected error!!!")
    return table, R

def main():
    if(len(sys.argv) != 3):
        print('Usage: python3 combine_outputs.py hyp1 hyp2')
        return
    hyp1 = sys.argv[1]
    hyp2 = sys.argv[2]
    align_corpus(hyp1, hyp2)

if __name__ == '__main__':
    main()
