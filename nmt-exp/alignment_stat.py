import sys
import pdb
from tqdm import tqdm
repo1 = '/home/alta/BLTSpeaking/ged-pm574/local/seq2seq/utils'
repo2 = '/home/alta/BLTSpeaking/exp-ytl28/local-ytl/py-tools/'
sys.path.insert(0, repo1)
sys.path.insert(0, repo2)

from levenshtein_align import levenshtein_align # repo1
import rdlextra_bias2right as rdlextra # repo2

# may need to install this package
# https://github.com/ztane/python-Levenshtein

def align_word_level(ref_sent, hyp_sent):
    # method 1
    a = ref_sent.split()
    b = hyp_sent.split()

    aout, bout = levenshtein_align(a,b)

    count = {'good': 0, 'sub': 0, 'ins': 0, 'del': 0}

    for a, b in zip(aout, bout):
        if a == b:
            count['good'] += 1
        elif '*' in b:
            count['del'] += 1
        else:
            if '*' in a:
                count['ins'] += 1
            else:
                count['sub'] += 1

    return count

def align_char_level(ref_sent, hyp_sent):
    a = ref_sent.split()
    b = hyp_sent.split()

    count = {'good': 0, 'sub': 0, 'ins': 0, 'del': 0}
    
    if len(a) == 0 and len(b) == 0:
        return count

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



    for a, b in zip(alis, blis):

        if a == b:
            count['good'] += 1
        elif '*' in b:
            count['del'] += 1
        else:
            if '*' in a:
                count['ins'] += 1
            else:
                count['sub'] += 1
    return count


def alignment_files(ref_file, hyp_file, align_method):
    with open(ref_file, 'r') as file:
        ref_sentences = file.readlines()
    with open(hyp_file, 'r') as file:
        hyp_sentences = file.readlines()

    if len(ref_sentences) != len(hyp_sentences):
        raise Exception('num sentences not match')

    total_count = {'good': 0, 'sub': 0, 'ins': 0, 'del': 0}

    l = len(ref_sentences)

    for i in tqdm(range(l)):
        s1 = ref_sentences[i].strip()
        s2 = hyp_sentences[i].strip()

        count = align_method(s1,s2)

        total_count['good'] += count['good']
        total_count['sub'] += count['sub']
        total_count['ins'] += count['ins']
        total_count['del'] += count['del']

    print("good =", total_count['good'])
    print("sub =", total_count['sub'])
    print("ins =", total_count['ins'])
    print("del =", total_count['del'])

    print("---------------------------------------------")

    print("%error = {:.2f}".format((total_count['sub']+total_count['ins']+total_count['del'])/total_count['good']*100))
    print("%sub = {:.2f}".format(total_count['sub']/total_count['good']*100))
    print("%ins = {:.2f}".format(total_count['ins']/total_count['good']*100))
    print("%del = {:.2f}".format(total_count['del']/total_count['good']*100))

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
