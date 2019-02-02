#!/bin/tcsh
# Check Number of Args
if ( $#argv != 3 )  then
   echo "Usage: $0 exam workdir tgt"
   exit 100
endif

set EXAM=$1
set WORKDIR=$2
set TGT=$3

set CLCBASE=/home/alta/CLC/LNRC/exams
set SRC=$CLCBASE/$EXAM

foreach f (`ls -l $SRC/*.corr | sed "s/.*\///" | sed -r "s/\.[^.]*//"`)
  cat $WORKDIR/$EXAM/$f/file.src >> $TGT/$EXAM.src
  cat $WORKDIR/$EXAM/$f/file.tgt >> $TGT/$EXAM.tgt
end
