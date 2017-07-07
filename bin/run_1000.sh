#!/bin/bash

#if [ $# -ne 2 ]; then
#		echo "usage: ./msma.sh <K value> <total number of runs>"
#		exit
#fi

#for ((i=2;i<=$1;i=i*2)) 
#do

# SYNTAX: run_1000.sh <K value> <number of discrete factors> <number of continuous factors> <number of interaction factors> <number of runs> <mixed or pure(0,1)>
	for ((j=1;j<=$5;j++))
	do
		echo K = $1, Run = $j
		cd ../new/
	    (time octave msma.m $1 $2 $3 $4 $6) 2>&1 | tee -a ../logs/dumpMSMA-K$1-D$2-C$3-I$4-R$5.txt 
		printf "\n\n"
	done
#done

