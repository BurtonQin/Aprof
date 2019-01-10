#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
compare runtime of targets
'''

import argparse
import os
import pandas as pd
from pathlib import Path
import subprocess
import time
try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

PROJECT_DIR="/home/boqin/Projects/Aprof"

CASE_NAME = './inputs/input_case_{0}.txt'
CONSTANT_SONG = 'song'

# Gen input str of i length into input_case_{i}.txt.
# input str: a{i}song
def generate_input(i):

	file_name = CASE_NAME.format(i)
	with open(file_name, 'w') as f:
		context = ('a' * i) + CONSTANT_SONG
		f.write(context)

	return file_name


# exec 'target file_name song' and record runtime.
# @param target: the exe file, used to test runtime
# @param result: the result file, store runtime results
def run_time_command(target, result, my_env=None):

	print(target)

#	output_path = "tmp.txt"
#	outfile = open(output_path, "w")
	
	inputs = []
	exe_times = []
	for i in range(1000, 10000, 500):
		for x in range(1):
			inputs.append(i)
			file_name = generate_input(i)
			command = [target, file_name, CONSTANT_SONG]
			start = time.time()
			if my_env:
				subprocess.run(command, stdout=DEVNULL, env=my_env, check=True)
				#subprocess.run(command, stdout=outfile, env=my_env, check=True)
				#subprocess.run(command, env=my_env, check=True)
			else:
				subprocess.run(command, stdout=DEVNULL, check=True)
				#subprocess.run(command, stdout=outfile, check=True)
				#subprocess.run(command, env=my_env, check=True)
			exe_times.append('%.5f' % (time.time() - start))
		dump_mem()
	
		df = pd.DataFrame(data={'inputs': inputs, 'time': exe_times})
		df.to_csv(result, index=False)
	
		sum = 0.0
		for t in exe_times:
			sum += float(t)
		print('%.5f' % (sum/len(exe_times)))
	
	#	outfile.close()


# cd build; make -f ../Makefile.clonesample OP_LEVEL=2 ELSEIF=-bElseIf install; cd ..
# @param nopass: nopass instead of clonesample
# @param O: op level
# @param bElseIf: if-elseif-else instead of if-else
def build_and_install():
	
	path = './build'
	Path(path).mkdir(exist_ok=True)
	
	prev_cwd = Path.cwd()
	os.chdir(path)
		
	subprocess.run(['make', '-f', '../Makefile', 'install'], stdout=DEVNULL, check=True)
	os.chdir(prev_cwd)
	

# run and record time in result, print avg
# @param nopass: nopass instead of clonesample
# @param O: op level
# @param bElseIf: if-elseif-else instead of if-else
def run_get_time():

	target_dir = './bin'
	result_dir = './results'

	target = os.path.join(target_dir, 'target')
	result = os.path.join(result_dir, 'runtime_result.csv')

	run_time_command(target, result)


# dump shared mem to logger
def dump_mem():
	
	logger = os.path.join(PROJECT_DIR, "cmake-build-debug/runtime/AprofLogger/AprofLogger")
	subprocess.run([logger], check=True)


# collect log into one
def collect_log():

	mem_result = './results/mem_result.csv'

	subprocess.run("echo func_id,rms,cost,chains > " + mem_result, shell=True)
	subprocess.run("cat aprof_logger_* | grep -v func_id >> " + mem_result, shell=True)
	subprocess.run('rm aprof_logger_*', shell=True)


# mkdir bin build inputs results
def make_dir():
	
	subprocess.run("mkdir -p bin build inputs results", shell=True)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("-onlyrun", help="no build, only run", action="store_true")
	args = parser.parse_args()

	make_dir()
	
	if (not args.onlyrun):
		build_and_install()
	run_get_time()

	collect_log()
