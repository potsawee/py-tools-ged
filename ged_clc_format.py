#!/usr/bin/python
'''
Create the CLC training data of different formats
for DTAL transcription GED experiment

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

    original = sys.argv[1]
    outdir = sys.argv[2]
    name = sys.argv[3]
    extension = sys.argv[4].strip('.')


    processor = GedProcessor(columns=['token', 'label'])
    processor.read(original)

    # file1
    file1 = outdir + '/' + name + '.marek.' + extension
    processor.basiccase(input=processor.original)
    processor.write(file1)

    # file2
    file2 = outdir + '/' + name + '.tlc.' + extension
    processor.truelowercase(input=processor.original)
    processor.write(file2)

    # file3
    file3 = outdir + '/' + name + '.nopunc.' + extension
    processor.period_only(input=processor.current)
    processor.write(file3)


if __name__ == "__main__":
    print(__doc__)
    main()
