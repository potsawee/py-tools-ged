#!/usr/bin/python3
'''
Combine the predictions of multiple files (GED outputs) in the target folder
Make a single file where the probablities are the Arithmetic Mean of the orignal ged outputs

Args:
    dir: Directory where the output of the GED system are located - only looks for .tsv files
    
Return:
    dir/combined-all.tsv
'''

import sys
import os

def combine(lines_list, output):
    num = len(lines_list)
    with open(output, 'w') as file:
        for i, line in enumerate(lines_list[0]):
            if line == '\n':
                file.write('\n')
                continue

            items = line.split()
            i_prob = 0
            for j in range(num):
                i_prob += float(lines_list[j][i].split()[-1].strip(':i'))

            i_prob /= num
            c_prob = 1.0 - i_prob

            new_line = '\t'.join(items[:-2])
            new_line += '\tc:{:.7f}'.format(c_prob)
            new_line += '\ti:{:.7f}'.format(i_prob)
            new_line += '\n'

            file.write(new_line)

def main():
    if(len(sys.argv) != 2):
        print('Usage: python3 combine_preds.py dir')
        return

    ged_out_path = sys.argv[1]

    files = [os.path.join(ged_out_path, f) for f in os.listdir(ged_out_path) if (os.path.isfile(os.path.join(ged_out_path, f))) and '.tsv' in f]
    print(files)
    files.sort()
    exp_path = os.path.dirname(ged_out_path)
    output = exp_path + "/combined-all.tsv"


    lines_list = []

    for i, file in enumerate(files):
        with open(file, 'r') as f:
            lines = f.readlines()
            lines_list.append(lines)

    length = len(lines_list[0])
    for i, lines in enumerate(lines_list[1:]):
        assert length == len(lines), "The legnth of {} is invalid - {} != {}".format(files[i+1], length, len(lines))

    combine(lines_list, output)

    print("Combining Done")

if __name__ == '__main__':
    main()
