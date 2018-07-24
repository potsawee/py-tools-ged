#!/usr/bin/python

'''
Visualise the score (probability of each word being grammatically incorrect)
predicted by the GED model.
'''

import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def visualise(path, start, l=20):
    df = pd.read_csv(path, delim_whitespace=True, header=None)
    df.columns = ['token', 'error_type' ,'label', 'c_prob', 'i_prob']
    c_probs = []
    i_probs = []
    for idx, row in df.iterrows():
        c_prob = float(row['c_prob'].replace('c:',''))
        c_probs.append(c_prob)
        i_probs.append(1-c_prob)
    df.drop(['c_prob','i_prob'], axis = 1, inplace=True)
    df['c_prob'] = c_probs
    df['i_prob'] = i_probs


    end = start+l

    plt.figure(figsize=(12,6))
    for token, label, x, y in zip(df[start:end]['token'], df[start:end]['label'], range(l), df[start:end]['i_prob']):
        plt.annotate(
            token + ' (' + label + ')',
            xy=(x, y), xytext=(10, -15),
            textcoords='offset points', ha='right', va='bottom')
    plt.plot(range(l), df[start:end]['i_prob'], 'o-')
    plt.axhline(0.5, color='darkorange')
    plt.ylim(ymax = 1.0, ymin = 0.0)
    plt.ylabel('Error Probability')
    plt.show()

def main():
    if(len(sys.argv) != 2):
        print('Usage: python3 visualise_ged_out.py ged_out_file')
        return

    file_path = sys.argv[1]
    my_file = Path(file_path)
    if not my_file.is_file():
        print(file_path + ': not exist')
        return

    c = 'y'
    while(c != 'n'):
        inp = input('Start index [length]: ')
        if(len(inp.split()) > 1):
            x = int(inp.split()[0])
            l = int(inp.split()[1])
            visualise(file_path, x, l)
        else:
            x = int(inp)
            visualise(file_path, x)

        c = input('Continue (y/n): ')

if __name__ == '__main__':
    main()
