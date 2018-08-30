#!/usr/bin/python3
'''
Create the ged-input files of different formats
for DTAL transcription GED experiment

Args:
    original: the original transcription e.g. /home/alta/BLTSpeaking/ged-kmk/cued/data/A1/inputs/train.tsv
    outdir: where the output will be located

Output:
    [0] original + remove hesitation + PW   => file0.tsv
    [1] file0 + basiccase              => ### file1.tsv / 1-Marek.tsv ###
    [2] file0 + truelowercase          => ### file2.tsv / 2-TLC.tsv ###
    [3] file2 + period_only            => ### file3.tsv / 3-NO-PUNC.tsv ###
    [4] file3 + Remove DM, RE, FS      => ### file4.tsv / 4-Remove-DM-RE-FS.tsv ###
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


    # processor = GedProcessor(columns=['token', 'error_type', 'label'])
    # To run an ASR experiment having the confidence column use this:
    processor = GedProcessor(columns=['token', 'error_type', 'confidence', 'label'])

    processor.read(original)

    # file0
    file0path = outdir + '/file0.tsv'
    os.makedirs(os.path.dirname(file0path), exist_ok=True)
    processor.remove_hesitation()
    processor.remove_partial()
    file0 = processor.current
    processor.write(file0path)

    #file1 - Marek
    file1path = outdir + '/file1.tsv'
    processor.basiccase()
    processor.write(file1path)

    #file2 - TLC
    file2path = outdir + '/file2.tsv'
    processor.truelowercase(input=file0, start_tag='</s>', end_tag='</s>')
    processor.write(file2path)

    #file3 - NO-PUNC
    file3path = outdir + '/file3.tsv'
    processor.period_only()
    processor.write(file3path)

    #file4-1 - REMOVE-DM
    file41path = outdir + '/file4-1.tsv'
    processor.remove_dm()
    processor.write(file41path)

    #file4-2 - REMOVE-DM-RE
    file42path = outdir + '/file4-2.tsv'
    processor.remove_re()
    processor.write(file42path)

    #file4-3 - REMOVE-DM-RE-FS
    file43path = outdir + '/file4-3.tsv'
    processor.remove_fs()
    processor.write(file43path)


if __name__ == "__main__":
    print(__doc__)
    main()
