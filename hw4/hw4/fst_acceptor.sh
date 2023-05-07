#!/bin/sh

fst=$1
input=$2

cat $input | while read line
do
	ans=`echo "$line" | carmel -slibEOk 1 $fst`
	if [ "$ans" = "0" ];
	then
		echo -e "$line\t=>\t*none* 0"
	else
		python3.4 count_prob.py $ans
		echo -e "$line\t=>\t$ans"
	fi

done
