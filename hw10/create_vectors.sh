#!/bin/sh
ARGS="${@:4}"
echo $ARGS;
/opt/python-3.6.3/bin/python3  create_vector.py --train_file "$1" --test_file "$2" --ratio "$3" --dirs "${ARGS}"