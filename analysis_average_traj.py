#!/usr/bin/env python2.7
import shlex
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Average over many .xvg energy trajectory files to get the average E(t) and S(t).')
parser.add_argument('--files', dest='file_list', nargs='+', type=str, help='a collection of all of the files to be averaged over')
parser.add_argument('-n', dest='total_time', type=int, default=0, help='the total number of time steps to average over. Overwritten by the number of time steps in the first file opened if this is smaller.')

args = parser.parse_args()
istimelimit = 0;
if (args.total_time != 0):
	istimelimit = 1

e_t = list()
time = list()

file_count = 0;
for fname in args.file_list:
	print 'NEW FILE: ' + fname
	n = 0
	with open(fname, 'r') as f:
		e_t_temp = list()
		for line in f:
			if (istimelimit and n >= args.total_time):
				break
			if (line[0] != '#' and line[0] != '@'):
				cols = shlex.split(line);
				n = n+1
				if (file_count == 0):
					e_t.append(float(cols[1]))
					time.append(float(cols[0]))
				else:
					e_t_temp.append(float(cols[1]))
		if (file_count == 0):
			e_t = np.array(e_t)
			time= np.array(time)
		else:
			e_t = e_t + np.array(e_t_temp)
		file_count = file_count + 1;


print [e_t / file_count, time]


