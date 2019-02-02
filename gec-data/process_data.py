import string
import sys
import re
from nltk.tokenize import word_tokenize

punc_list = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' # string.punctuation

def main():
    if(len(sys.argv) != 3):
        print('Usage: python3 process_data.py input output')
        return

    inp = sys.argv[1]
    oup = sys.argv[2]
    out_lines = []

    with open(inp, 'r') as file1:
        out_line = []
        prev_id = None
        for line in file1:

            words = word_tokenize(line)

            cur_id = words[0]
            if not cur_id[-1].isdigit():
                cur_id = cur_id[:-1]
            if cur_id != prev_id:
                if prev_id != None:
                    out_lines.append(out_line)
                out_line = []
                prev_id = cur_id

            for word in words[1:]:
                if word in punc_list:
                    pass
                else:
                    out_line.append(word.lower())

    with open(oup, 'w') as file2:
        for line in out_lines:
            file2.write(' '.join(line) + ' .\n')
            # file2.write(' '.join(line) + ' \n')

if __name__ == '__main__':
    main()
