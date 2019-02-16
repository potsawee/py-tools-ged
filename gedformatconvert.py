import sys

def one_word_to_one_sentence(input, output):
    with open(input, 'r') as f1:
        with open(output, 'w') as f2:
            newline = []
            for line in f1:
                if line == '\n':
                    if len(newline) > 0:
                        f2.write(' '.join(newline) + '\n')
                    newline = []
                else:
                    word = line.strip().split()[0]
                    # ----------- Filter ----------- #
                    # for swb work - 8 Feb 2019
                    # disf = line.strip().split()[1]
                    # if disf != 'O':
                    #     continue
                    # ------------------------------ #
                    newline.append(word)
    print('convert one_word_to_one_sentence done!')



def one_sentence_to_one_word(input, output):
    with open(input, 'r') as f1:
        with open(output, 'w') as f2:
            newline = []
            for line in f1:
                # if line == '\n':
                #     if len(newline) > 0:
                #         f2.write(' '.join(newline) + '\n')
                #     newline = []
                # else:
                #     word = line.strip().split()[0]
                #     newline.append(word)
                words = line.split()
                for word in words:
                    f2.write(word + '\n')
                f2.write('\n')
    print('convert one_sentence_to_one_word done!')

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 gedformatconvert.py [1/2] input output")
        return

    convert_type = sys.argv[1]
    input = sys.argv[2]
    output = sys.argv[3]

    if convert_type == '1':
        one_word_to_one_sentence(input, output)
    elif convert_type == '2':
        one_sentence_to_one_word(input, output)

if __name__ == '__main__':
    main()
