#!/bin/sh
lm_file=$1
l1=$2
l2=$3
l3=$4
test_data=$5
output_file=$6
/opt/python-3.6/bin/python3 ./perplexity.py $lm_file $l1 $l2 $l3 $test_data $output_file