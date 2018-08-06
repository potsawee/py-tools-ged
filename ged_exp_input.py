#!/usr/bin/python3
'''
Create the ged-input files of different formats
for DTAL transcription GED experiment

[0] original + remove hesitation   => file0.tsv
[1] file0 + basiccase              => ### 1-Marek.tsv ###
[2] file0 + truelowercase          => ### 2-TLC.tsv ###
[3] file2 + period_only            => ### 3-NO-PUNC.tsv ###
[4] file3 + remove_repetition      => ### 4-Remove-RE.tsv ###
'''
import os
import sys
from gedprocessor import GedProcessor

def main():
    if(len(sys.argv) != 3):
        print("Usage: python3 ged_exp_input.py original outdir")
        return

    original = sys.argv[1]
    outdir = sys.argv[2]

    processor = GedProcessor(columns=['token', 'error_type', 'label'])
    processor.read(original)

    # file0
    file0path = outdir + '/file0.tsv'
    os.makedirs(os.path.dirname(file0path), exist_ok=True)
    processor.remove_hesitation()
    file0 = processor.current
    processor.write(file0path)

    #file1 - Marek
    file1path = outdir + '/file1.tsv'
    processor.basiccase()
    processor.write(file1path)

    #file2 - TLC
    file2path = outdir + '/file2.tsv'
    processor.truelowercase(input=file0)
    processor.write(file2path)

    #file3 - NO-PUNC
    file3path = outdir + '/file3.tsv'
    processor.period_only()
    processor.write(file3path)

    #file4 - REMOVE-RE
    file4path = outdir + '/file4.tsv'
    processor.remove_repetition()
    processor.write(file4path)

if __name__ == "__main__":
    print(__doc__)
    main()
