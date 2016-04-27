#!/bin/bash

# Automatically run a bunch of ycsb tests
# author: Jiexi Lin <jiexil@andrew.cmu.edu>
# date: April 26th, 2016

if [ $# -ne 3 ]; then
	echo "$0 <prefix> <res_dir> <peloton_git_root>"
	exit
fi

RESDIR="$2"
OUTPUTFILE="outputfile.summary"
PELOTONDIR="$3"
WORKDIR="$PELOTONDIR/build"
GCSRCDIR="$PELOTONDIR/src/backend/gc"
GCFAC_H="$GCSRCDIR/gc_manager_factory.h"
GC_H="$GCSRCDIR/gc_manager.h"
TXNFAC_CPP="$PELOTONDIR/src/backend/concurrency/transaction_manager_factory.cpp"
PWD=`pwd`

PREFIX=$1
GC=ON
ATTEMPT=100000

cd $WORKDIR

# modify the src code and remake
sed -i "s/ON/${GC}/g" $GCFAC_H
sed -i "s/OFF/${GC}/g" $GCFAC_H

sed -i "s/MAX_ATTEMPT_COUNT [0-9].*/MAX_ATTEMPT_COUNT $ATTEMPT/g" $GC_H

../configure && make clean

for m in "PESSIMISTIC" "OPTIMISTIC" "SPECULATIVE_READ" "EAGER_WRITE" "SSI" "TO"
do
	# modify the txn manager and compile
	sed -i "s/CONCURRENCY_TYPE_.*/CONCURRENCY_TYPE_${m};/g" $TXNFAC_CPP
	make -j
	if [ $? -ne 0 ]; then
		echo "Make failed"
		exit
	fi
	
	for b in 2 4 8 12 16 20 24
	do
		for k in 1 2 4 8 16 24
		do
			echo "./src/ycsb -b $b -k $k > /dev/null"
			./src/ycsb -b $b -k $k > /dev/null
			echo "cp $OUTPUTFILE $RESDIR/${PREFIX}_${m}_b${b}_k${k}"
			cp $OUTPUTFILE $RESDIR/${PREFIX}_${m}_b${b}_k${k}
		done
	done
done
cd $PWD
