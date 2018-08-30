import nltk

def main():
    while True:
        text = input("Text: ")
        text_tokenized = nltk.word_tokenize(text)
        pos_tags = nltk.pos_tag(text_tokenized)
        pos_tags = [pos_tag[1] for pos_tag in pos_tags]
        print("POS: ", '  '.join(pos_tags))

if __name__ == "__main__":
    main()
