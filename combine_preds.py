#!/usr/bin/python3
import sys

def write_avg_am(lines1, lines2, output):
    with open(output, 'w') as f:
        for l1, l2 in zip(lines1, lines2):
            if(l1 == '\n' and l2 == '\n'):
                f.write('\n')
                continue

            items1 = l1.split()
            items2 = l2.split()

            c_avg = 0.5 * ( float(items1[-2].strip(':c')) + float(items2[-2].strip(':c')) )
            i_avg = 0.5 * ( float(items1[-1].strip(':i')) + float(items2[-1].strip(':i')) )

            new_line = '\t'.join(items1[:-2])
            new_line += '\tc:{:.7f}'.format(c_avg)
            new_line += '\ti:{:.7f}'.format(i_avg)
            new_line += '\n'

            f.write(new_line)

def write_avg_2(lines1, lines2, output):
    with open(output, 'w') as f:
        for l1, l2 in zip(lines1, lines2):
            if(l1 == '\n' and l2 == '\n'):
                f.write('\n')
                continue

            items1 = l1.split()
            items2 = l2.split()

            i2 = float(items2[-1].strip(':i'))

            if i2 > 0.9 or i2 < 0.1:
                c_avg = 0.5 * ( float(items1[-2].strip(':c')) + float(items2[-2].strip(':c')) )
                i_avg = 0.5 * ( float(items1[-1].strip(':i')) + float(items2[-1].strip(':i')) )
            else:
                c_avg = float(items1[-2].strip(':c'))
                i_avg = float(items1[-1].strip(':i'))

            new_line = '\t'.join(items1[:-2])
            new_line += '\tc:{:.7f}'.format(c_avg)
            new_line += '\ti:{:.7f}'.format(i_avg)
            new_line += '\n'

            f.write(new_line)


def main():
    if(len(sys.argv) != 5):
        print('Usage: python3 combine_preds.py file1 file2 output option')
        return

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output = sys.argv[3]
    option = sys.argv[4]

    # file1 = "/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/noattention-fcepub.ged.spell.v2.tsv"
    # file2 = "/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/multihead1-fcepub.ged.spell.v2.tsv"
    # output = "/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/no-attention-multihead1-avg.ged.spell.v2.tsv"

    with open(file1, 'r') as f1:
        lines1 = f1.readlines()
    with open(file2, 'r') as f2:
        lines2 = f2.readlines()

    assert len(lines1) == len(lines2), "Both files must have the same number of lines. {} != {}".format(len(lines1), len(lines2))

    # Arithmetic  mean (AM)
    if(option == "am"):
        write_avg_am(lines1, lines2, output)
        print("Combining Mean Average done!")
    elif(option == "my2"):
        write_avg_2(lines1, lines2, output)
        print("Combining my 2 done!")
if __name__ == '__main__':
    main()
