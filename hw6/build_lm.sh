#!/bin/sh
ngram_count_file=$1
lm_file=$2
/opt/python-3.6/bin/python3 ./build_lm.py $ngram_count_file $lm_file