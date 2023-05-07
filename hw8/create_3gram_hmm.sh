#!/bin/sh
output=$1
l1=$2
l2=$3
l3=$4
unk_prob=$5
/opt/python-3.6/bin/python3 ./hmm_3gram.py $output $l1 $l2 $l3 $unk_prob