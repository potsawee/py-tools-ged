import sys

# /home/dawna/material/Kaldi_V0.1/base/tools/text-to-count.py
# use this script to count words first

def build_vocab1(countfile, min_count=3, lower=True):

    vocab_list = set()

    # special_tokens = ['<unk>', '<s>', '</s>', '<go>']
    # special_tokens = []

    with open(countfile, 'r') as file:
        for line in file:
            count, word  = line.strip().split()
            count = int(count)
            if count >= min_count:
                word = word.lower()
                print(word)

def main():
    if(len(sys.argv) < 2):
        print('Usage: python3 build_vocab_list.py countfile')
        return

    countfile = sys.argv[1]

    build_vocab1(countfile, min_count=3, lower=True)

if __name__ == "__main__":
    main()
