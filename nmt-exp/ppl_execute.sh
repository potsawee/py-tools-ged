#!/bin/tcsh
#$ -S /bin/tcsh

# Check Number of Args
# if ($#argv != 2) then
#    echo "Usage: $0 testfile outputfile"
#    exit 100
# endif

# set TESTFILE=$1
# set OUTPUTFILE=$2

set FILE=/home/alta/BLTSpeaking/ged-pm574/nmt-exp/swb-work/fluency/train_asr_withI
set TESTFILE=$FILE.stag
set OUTPUTFILE=$FILE.ppl

set RNNLMBIN=/home/dawna/material/Tools_V1.3/lbin/rnnlm
set MODEL=/home/alta/BLTSpeaking/ged-pm574/gec-lm/train-rnnlm/rnnlms/v3/one-billion/RNN_weight.OOS.cuedrnnlm.rnnlm.300.300/train_LM.wgt.iter9
set INPUTWLIST=/home/alta/BLTSpeaking/ged-pm574/gec-lm/train-rnnlm/rnnlms/v3/one-billion/lib/wlists/train.lst.index
set OUTPUTWLIST=/home/alta/BLTSpeaking/ged-pm574/gec-lm/train-rnnlm/rnnlms/v3/one-billion/lib/wlists/train.lst.index
set VOCABSIZE=64002

$RNNLMBIN -ppl \
-readmodel $MODEL \
-testfile $TESTFILE \
-inputwlist $INPUTWLIST \
-outputwlist $OUTPUTWLIST \
-fullvocsize $VOCABSIZE \
-debug 2 > $OUTPUTFILE
