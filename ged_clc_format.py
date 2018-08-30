#!/usr/bin/python3
'''
Create the CLC training data of different formats
for DTAL transcription GED experiment

Args:
    original: original .ged.tsv file
    outdir: target directory
    name: target name
    extention: target extension

Output:
    [1] original + basiccase         => Marek / Firstcase format
    [2] original + truelowercase     => TLC (true lowercase) format
    [3] TLC + period_only            => TLC & No punctuation
'''

import os
import sys
from gedprocessor import GedProcessor

def main():
    if(len(sys.argv) != 5):
        print("Usage: python3 ged_clc_format.py original outdir name extention")
        return

    print(__doc__)

    original = sys.argv[1]
    outdir = sys.argv[2]
    name = sys.argv[3]
    extension = sys.argv[4].strip('.')


    processor = GedProcessor(columns=['token', 'error_type','label'])
    processor.read(original)

    # file1
    # file1 = outdir + '/' + name + '.marek.' + extension
    # processor.basiccase(input=processor.original)
    # processor.write(file1)

    # file2
    file2 = outdir + '/' + name + '.tlc.' + extension
    processor.truelowercase(input=processor.original, start_tag="</s>", end_tag="</s>")
    processor.write(file2)

    # file3
    file3 = outdir + '/' + name + '.nopunc.' + extension
    # processor.period_only(input=processor.current) # .period_only remove punc without propagating 'i'
    processor.remove_punctuation(input=processor.current)

    processor.write(file3)


if __name__ == "__main__":
    main()
