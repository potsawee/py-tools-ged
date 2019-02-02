#!/bin/tcsh

# Check Number of Args
if ( $#argv != 3 )  then
   echo "Usage: $0 exam file tgtdir"
   exit 100
endif

set EXAM=$1
set FILE=$2
set TGTDIR=$3

set ORIG=/home/alta/CLC/LNRC/exams/$EXAM/$FILE
set TGT=$TGTDIR/$EXAM/$FILE
set PROCESSOR=/home/alta/BLTSpeaking/ged-pm574/local/py-tools/gec-data/process_data.py

if (! -d $TGT) mkdir -p $TGT

echo "-----------------------------------------------------"
echo "file: $ORIG"
echo "-----------------------------------------------------"

python3 $PROCESSOR $ORIG.corr $TGT/file.src
echo "convert corr (source) done"
python3 $PROCESSOR $ORIG.spell $TGT/file.tgt
echo "convert spell (target) done"



if ( `wc -l < $TGT/file.src` == `wc -l < $TGT/file.tgt` ) then
    # echo 'Lines SRC == TGT'
    exit 100
else
    echo "Warning: Line numbers not match $TGT"
    exit
endif
