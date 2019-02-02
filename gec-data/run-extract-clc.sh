#!/bin/tcsh

# Check Number of Args
if ( $#argv != 2 )  then
   echo "Usage: $0 exam tgtdir"
   exit 100
endif

set EXAM=$1
set TGTDIR=$2

set EXTRACT=/home/alta/BLTSpeaking/ged-pm574/local/py-tools/gec-data/extract-clc.sh
set CLCBASE=/home/alta/CLC/LNRC/exams
set SRC=$CLCBASE/$EXAM

foreach f (`ls -l $SRC/*.corr | sed "s/.*\///" | sed -r "s/\.[^.]*//"`)
    $EXTRACT $EXAM $f $TGTDIR
end
