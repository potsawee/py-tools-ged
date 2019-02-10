#!/bin/tcsh
#$ -S /bin/tcsh

set verbose

# Check Number of Args
if ($#argv != 2) then
   echo "Usage: $0 inpath outname"
   exit 100
endif

set INPUT=$1
set FILE=$2
set PPLPARSER=/home/alta/BLTSpeaking/ged-pm574/local/py-tools/nmt-exp/ppl_parser.py
set PROC1=/home/alta/BLTSpeaking/ged-pm574/local/py-tools/nmt-exp/add-remove-fullstop.py
set PROC2=/home/alta/BLTSpeaking/ged-pm574/local/py-tools/lower_file.py
set FIXUNK=/home/alta/BLTSpeaking/ged-pm574/local/seq2seq/utils/replace_unk.py
set ALIGN=/home/alta/BLTSpeaking/ged-pm574/local/py-tools/nmt-exp/alignment.py

python3 $PPLPARSER 1 $FILE.ppl > $FILE.score
python3 $PPLPARSER 2 $FILE.out $FILE.score > $FILE.oneout
python3 $PROC1 stagremove $FILE.oneout > $FILE.notag
python3 $PROC2 $FILE.notag > $FILE.corrupted
python3 $FIXUNK $INPUT $FILE.corrupted > $FILE.fixunk
python3 $ALIGN $INPUT $FILE.fixunk > $FILE.ged.tsv
