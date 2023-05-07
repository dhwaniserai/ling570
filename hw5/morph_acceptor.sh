#!/bin/sh
fst=$1
input=$2
output=$3
cat $input | while read line
do
	mline=$(python3.4 split_str.py $line)
	#echo "$mline"
	ans=`echo "$mline" | carmel -slibEOkWQ 1 $fst`
	if [ "$ans" = "0" ];
	then
		echo -e "$line\t=>\t*NONE*" >> $output
	else
		new_ans=$(python3.4 format_op.py $ans)
		echo -e "$line => $new_ans" >> $output
		#echo -e "$line\t=>\t$ans"
	fi

done