import string

class GedProcessor(object):
    def __init__(self, columns=['token', 'error_type', 'label']):
        self.columns = columns
        self.num_columns = len(columns)
        self.original = None
        self.current = None

    def read(self, path):
        with open(path, 'r') as file:
            lines = file.readlines()

        print("----------------------------------------")
        print("Original File: {}".format(path))
        print("----------------------------------------")

        original = []
        for i, line in enumerate(lines):
            if line == '\n':
                original.append(['\n'])
                continue
            items = line.split()
            if(len(items) != self.num_columns):
                print("Skip: Line {} - invalid number of fields\n=> {}".format(i,line))
                continue
            if(items[-1] != 'c' and items[-1] != 'i'):
                print("Skip: Line {} - invalid label\n=> {}".format(i, line))
                continue

            original.append(items)
            self.original = original
            self.current = original

    def remove_hesitation(self, input=None):
        processed = []
        if input == None:
            input = self.current

        for word in input:
            if word[0] == '\n':
                processed.append(word)
                continue
            if (word[0] == '%hesitation%'):
                continue
            processed.append(word)
        self.current = processed

    def period_only(self, input=None):
        punc_set = set(string.punctuation)
        processed = []
        if input == None:
            input = self.current

        for word in input:
            if word[0] == '\n':
                processed.append(word)
                continue
            if (word[0] in punc_set and word[0] != '.'):
                continue
            processed.append(word)
        self.current = processed

    def basiccase(self, input=None):
        # basiccase e.g. "The cat sat."
        # Capitalise first words
        # End each sentence with a full stop
        processed = []
        if input == None:
            input = self.current

        dot = ['.']
        dot += ['_'] * (self.num_columns - 2)
        dot += 'c'

        beginning = True
        for word in input:
            if word[0] == '\n':
                beginning = True
                processed.append(dot)
                processed.append(word)
                continue

            if word[0] == '.': # full stops at start/end added manually
                continue       # there should not be more full-stops

            if not beginning:
                if word[0] != 'i':
                    # processed.append(word)
                    w = word[0].lower()
                    processed.append([w] + word[1:])
                else: # 'i' => 'I'
                    processed.append(['I'] + word[1:])
            else:
                processed.append([word[0].capitalize()] + word[1:])
                beginning = False

        self.current = processed

    def truelowercase(self, input=None, start_tag='.', end_tag='.'):
        # truelowercase e.g. ". the cat sat ."
        # All lowercased
        # Start/End with full stops
        processed = []
        if input == None:
            input = self.current

        front = [start_tag]
        front += ['_'] * (self.num_columns - 2)
        front += 'c'
        back = [end_tag]
        back += ['_'] * (self.num_columns - 2)
        back += 'c'

        sentence = []

        for word in input:
            if word[0] == '\n':
                processed.append(front)
                processed += sentence
                processed.append(back)
                processed.append(word)
                sentence = []
                continue

            if word[0] == '.': # full stops at start/end added manually
                continue       # there should not be more full-stops

            w = word[0].lower()
            sentence.append([w] + word[1:])

        self.current = processed

    def remove_repetition(self, input=None):
        processed = []
        if input == None:
            input = self.current

        processed = [input[0]]
        prev_w = input[0][0]
        prev_l = input[0][-1]

        for word in input:
            if word[0] == '\n':
                processed.append(word)
                prev_w = ''
                prev_l = ''
                continue

            cur_w = word[0]
            cur_l = word[-1]

            if cur_w != prev_w:
                processed.append(word)
            else: # repetition found!
                # TODO: make sure this is right!
                pass

            prev_w = cur_w
            prev_l = cur_l

        self.current = processed

    def write(self, outpath):
        with open(outpath, 'w') as file:
            for word in self.current:
                if len(word) == 1 and word[0] == '\n':
                    file.write('\n')
                else:
                    file.write('\t'.join(word) + '\n')
        print("writing {} done!".format(outpath))
