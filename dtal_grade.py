#!/usr/bin/python3
'''
Split the DTAL transcription by their grades

Args:
    - None BUT need to change the source code according the where the input/output are
    - TO USE:
        - change the orignal DTAL path
            e.g. path = "/home/alta/BLTSpeaking/ged-kmk/dtal/data/GEM4/indtsv"
        - change the A1, A2, B1, B2, C output paths
            e.g. a1 = "/home/alta/BLTSpeaking/ged-pm574/dtal/data/GEM4-grade-dependent/BLXXXeval3_annotator5_A1.tsv"
Output:
    - .ged.tsv split by grades
'''


import os
from convertor import Convertor

convertor = Convertor()
convertor.read_map(convertor.mapping_file1)
convertor.read_grade(convertor.grading_file1)

def main():
    path = "/home/alta/BLTSpeaking/ged-kmk/dtal/data/GEM4/indtsv"
    print('-------------------------------------------------------')
    print(path)
    print('-------------------------------------------------------')
    files = [os.path.join(path, f) for f in os.listdir(path) if (os.path.isfile(os.path.join(path, f))) and '.tsv' in f]
    files_a1 = []
    files_a2 = []
    files_b1 = []
    files_b2 = []
    files_c = []
    for file in files:
        grade = filename_to_grade(file)
        if(grade == 'A1'):
            files_a1.append(file)
        elif(grade == 'A2'):
            files_a2.append(file)
        elif(grade == 'B1'):
            files_b1.append(file)
        elif(grade == 'B2'):
            files_b2.append(file)
        elif(grade == 'C'):
            files_c.append(file)
        else:
            print(file, "KeyError")
    print('-------------------------------------------------------')
    print("A1:", len(files_a1))
    print("A2:", len(files_a2))
    print("B1:", len(files_b1))
    print("B2:", len(files_b2))
    print(" C:", len(files_c))

    a1 = "/home/alta/BLTSpeaking/ged-pm574/dtal/data/GEM4-grade-dependent/BLXXXeval3_annotator5_A1.tsv"
    a2 = "/home/alta/BLTSpeaking/ged-pm574/dtal/data/GEM4-grade-dependent/BLXXXeval3_annotator5_A2.tsv"
    b1 = "/home/alta/BLTSpeaking/ged-pm574/dtal/data/GEM4-grade-dependent/BLXXXeval3_annotator5_B1.tsv"
    b2 = "/home/alta/BLTSpeaking/ged-pm574/dtal/data/GEM4-grade-dependent/BLXXXeval3_annotator5_B2.tsv"
    c = "/home/alta/BLTSpeaking/ged-pm574/dtal/data/GEM4-grade-dependent/BLXXXeval3_annotator5_C.tsv"

    write_file(a1, files_a1)
    write_file(a2, files_a2)
    write_file(b1, files_b1)
    write_file(b2, files_b2)
    write_file(c, files_c)


def write_file(newfile, files):
    with open(newfile, 'w') as file:
        for f in files:
            with open(f) as infile:
                for line in infile:
                    file.write(line)


def filename_to_grade(filename):
    ce_id = os.path.basename(filename).split('_')[0]
    try:
        cued_id = convertor.ce_to_cued[ce_id]
        grade = convertor.cued_to_grade[cued_id]
        return grade
    except KeyError:
        return '?'


if __name__ == "__main__":
    main()
