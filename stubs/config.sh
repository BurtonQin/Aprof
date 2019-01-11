#!/usr/bin/env bash
# config PROJECT_DIR

PROJECT_DIR=$(realpath ../)

for filepath in $(ls ./*/Makefile)
do
	echo ${filepath}
	sed -i "s|PROJECT_DIR=.*|PROJECT_DIR=$PROJECT_DIR|" ${filepath}
done

for filepath in $(ls ./*/run_exe_time.py)
do
	echo ${filepath}
	sed -i "s|PROJECT_DIR=.*|PROJECT_DIR=\"$PROJECT_DIR\"|" ${filepath}
done
