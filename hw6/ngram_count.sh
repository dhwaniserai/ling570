#!/bin/sh
training_data=$1
ngram_count_file=$2
/opt/python-3.6/bin/python3 ./ngram_count.py $training_data $ngram_count_file