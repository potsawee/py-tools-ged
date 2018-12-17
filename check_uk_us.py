import sys
def main():
    path = sys.argv[1]
    path_to_us = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/wlists/us_spellings.txt"
    path_to_uk = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/wlists/uk_spellings.txt"
    us_to_uk_dict = {}
    uk_to_us_dict = {}
    with open(path_to_us, 'r') as file:
        us_wlist = file.readlines()
    with open(path_to_uk, 'r') as file:
        uk_wlist = file.readlines()
    for us_word, uk_word in zip(us_wlist, uk_wlist):
        us_to_uk_dict[us_word.strip()] = uk_word.strip()
    for us_word, uk_word in zip(us_wlist, uk_wlist):
        uk_to_us_dict[uk_word.strip()] = us_word.strip()

    uk_count = 0
    uk_words = []
    us_count = 0
    us_words = []
    other_count = 0

    with open(path, 'r') as file:
        for line in file:
            if line == '\n':
                continue
            word = line.split()[0].lower()
            if word in uk_to_us_dict:
                uk_count += 1
                if word not in uk_words:
                    uk_words.append(word)
            elif word in us_to_uk_dict:
                us_count += 1
                if word not in us_words:
                    us_words.append(word)
            else:
                other_count += 1

    print("UK count =", uk_count)
    print("US count =", us_count)
    print("other count =", other_count)

    for word in uk_words:
        print("UK: ", word)
    print('------------------------')
    for word in us_words:
        print("US: ", word)

if __name__ == '__main__':
    main()
