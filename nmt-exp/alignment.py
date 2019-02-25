"""
Word or Character Level Levenshtein Alignment
"""

import sys
import pdb
repo1 = '/home/alta/BLTSpeaking/ged-pm574/local/seq2seq/utils'
repo2 = '/home/alta/BLTSpeaking/exp-ytl28/local-ytl/py-tools/'
sys.path.insert(0, repo1)
sys.path.insert(0, repo2)

from levenshtein_align import levenshtein_align # repo1
import rdlextra_bias2right as rdlextra # repo2

# may need to install this package
# https://github.com/ztane/python-Levenshtein

def align_word_level(ref_sent, hyp_sent):
    a = ref_sent.split()
    b = hyp_sent.split()

    aout, bout = levenshtein_align(a,b)

    # if len(aout) != len(bout):
    #     print("Error!")
    #     pdb.set_trace()
    # tried! -> len(aout) equal len(bout)
    n = len(bout)
    labels = []

    # for a, b, label in zip(aout, bout, labels):
    for idx in range(n):
        a = aout[idx]
        b = bout[idx]

        if a == b: # correct
            labels.append('c')
        elif '*' in b: # deletion
            labels.append('<del>')
        else: # substitution or insertion
            labels.append('i')

    for idx in range(n-1):
        if labels[idx] == '<del>':
            labels[idx+1] = 'i'
    for a, b, label in zip(aout, bout, labels):
        if label != '<del>':
            print("{}\t{}\t{}".format(b, a, label))


def align_char_level(ref_sent, hyp_sent):
    a = ref_sent.split()
    b = hyp_sent.split()

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

    n = len(blis)
    labels = []
    for idx in range(n):
        a = alis[idx]
        b = blis[idx]

        if a == b: # correct
            labels.append('c')
        elif '*' in b: # deletion
            labels.append('<del>')
        else: # substitution or insertion
            labels.append('i')

    for idx in range(n-1):
        if labels[idx] == '<del>':
            # only look forward for one step! - I could change the code to look more
            # but that may lead to some unexpected problems
            if labels[idx+1] != '<del>':
                alis[idx+1] = alis[idx] + "+" + alis[idx+1]
                labels[idx+1] = 'i'
            else:
                pass

    for a1, b1, label in zip(alis, blis, labels):
        # label = 'c' if a1 == b1 else 'i'
        # print('{}\t{}\t{}'.format(a1,b1,label))
        # if '*' not in b1:
        if label != '<del>':
            print('{}\t{}\t{}'.format(b1,a1,label))


def alignment_files(ref_file, hyp_file, align_method):
    with open(ref_file, 'r') as file:
        ref_sentences = file.readlines()
    with open(hyp_file, 'r') as file:
        hyp_sentences = file.readlines()

    if len(ref_sentences) != len(hyp_sentences):
        raise Exception('num sentences not match')

    for s1, s2 in zip(ref_sentences, hyp_sentences):
        s1 = s1.strip()
        s2 = s2.strip()

        align_method(s1,s2)
        print()

def main():
    if(len(sys.argv) != 4):
        print('Usage: python3 alignment.py [word/char] original corrupted')
        return

    option = sys.argv[1] # word or char
    original = sys.argv[2]
    corrupted = sys.argv[3]

    if option not in ['word', 'char']:
        print('Usage: python3 alignment.py [word/char] original corrupted')
        return
    else:
        if option == 'word':
            align_method = align_word_level
        else:
            align_method = align_char_level

    alignment_files(original, corrupted, align_method)

if __name__ == '__main__':
    main()
