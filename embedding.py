import numpy as np
import pandas as pd
import csv

class Embedding(object):
    def __init__(self, path, skiprows=None):
        self.path = path
        self.words = pd.read_table(path, sep=" ", index_col=0, header=None, quoting=csv.QUOTE_NONE, skiprows=skiprows)
        self.words_matrix = self.words.as_matrix()

    def vec(self, word):
        if word not in self.words.index:
            print("{} not in the embedding model".format(word))
            return
        else:
            return self.words.loc[word].as_matrix()

    def find_closest_words(self, word, num=1):
        if word not in self.words.index:
            print("{} not in the embedding model".format(word))
            return
        diff = self.words_matrix - self.vec(word)
        delta = np.sum(diff * diff, axis=1)
        idx = np.argpartition(delta, num)
        # argpartition does not sort
        idx = idx[np.argsort(delta[idx])]
        for i in range(num):
            print("{}-th: {}".format(i+1, self.words.iloc[idx[i]].name))
