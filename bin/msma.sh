cd ../new/
if [ $# -ne 1 ]; then
	echo "usage: ./msma.sh <configNum> # between 1 and 16"
	exit
fi
time octave msma.m $1 
