#!/usr/bin/env bash
# config PROJECT_DIR

PROJECT_DIR=$(realpath ../)

FILE_NAMES=(Makefile run_exe_time.py)

for filename in ${FILE_NAMES[@]}
do
	for filepath in $(ls ./*/${filename})
	do
		echo ${filepath}
		sed -i "s|PROJECT_DIR=.*|PROJECT_DIR=\"$PROJECT_DIR\"|" ${filepath}
	done
done
