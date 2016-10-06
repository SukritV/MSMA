#!/bin/bash

#./run_1000.sh 4 3 1 0 1000
#./run_1000.sh 4 2 2 0 1000
#./run_1000.sh 4 1 3 0 1000
#./run_1000.sh 4 0 4 0 1000

#./run_1000.sh 4 3 1 0 50 1
#./run_1000.sh 4 3 1 0 100 1
#./run_1000.sh 4 3 1 0 250 1
#./run_1000.sh 4 3 1 0 500 1
#./run_1000.sh 4 3 1 0 750 1
#./run_1000.sh 4 3 1 0 1000 1


#./run_1000.sh 8 6 2 0 1000
#./run_1000.sh 8 5 3 0 1000
#./run_1000.sh 8 4 4 0 1000
#./run_1000.sh 8 3 5 0 1000
#./run_1000.sh 8 2 6 0 1000
#./run_1000.sh 8 1 7 0 1000
#./run_1000.sh 8 0 8 0 1000



run_array=(50 100 250 500 750 1000)
'
# CONTINUOUS & DISCRETE MIXED
for ((i=2;i<=2;i++))
do 
	for((j = 1;j<=i;j++))
	do
		let k=$i-$j
		for l in "${run_array[@]}"
		do 
			./run_1000.sh $i $k $j 0 $l 0
		done
	done
done
'

# DISCRETE ONLY
for ((i=3;i<=3;i++))
do 
	let k=$i-1
	for l in "${run_array[@]}"
	do 
		echo "./run_1000.sh $i $k 1 0 $l 1"
	done
done