from svmutil import *
from commonutil import *
from svm import *
from ctypes import *
import sys
import os
import re

x_space = []
cross_validation = None
nr_fold = None
model = None
param = None
prob = None
line = None

def exit_input_error(line_num):
	print("Wrong input format at line %d\n", %line_num)
	exit(1)

def do_cross_validation():
	total_correct = 0
	total_error = 0
	sumv = 0
	sumy = 0
	sumvv = 0
	sumyy = 0
	sumvy = 0
	target = (c_double * prob.l)()

	libsvm.svm_cross_validation(prob, param, nr_fold, target)
	if(param.svm_type == EPSILON_SVR || param.svm_type == NU_SVR):
		for i in range(0, prob.l):
			y = prob.y[i]
			v = target[i]
			total_error += (v-y)**2
			sumv += v
			sumy += y
			sumvv += v**2
			sumyy += y**2
			sumvy = v*y
		print("Cross Validation Mean Squared Error = %g\n" %total_error/prob.l)
		print("Cross Validation Squared Correlation Coefficient = %g\n" %(((prob.l*sumvy-sumv*sumy)*(prob.l*sumvy-sumv*sumy))/
			((prob.l*sumvv-sumv*sumv)*(prob.l*sumyy-sumy*sumy))))
	else:
		for i in range(0, prob.l):
			if(target[i] == prob.y[i]):
				total_correct +=1
		print("Cross Validation Accuracy = %g%%\n" %(100.0*total_correct/prob.l))

def parse_command_line():
	param = svm_parameter()
	param.set_to_default_values()
	print_func = cast(None, PRINT_STRING_FUN)
	i = 1
	while i < len(sys.argv):
		if(sys.argv[i][0] != '-'):
			break
		if(i >= len(sys.argv)):
			exit(1)
		i+=1
		target = sys.argv[i-1][1]
		if(target == 's'):
			param.svm_type = int(sys.argv[i])
		elif(target == 't'):
			param.kernel_type = int(sys.argv[i])
		elif(target == 'd'):
			param.degree = int(sys.argv[i])
		elif(target == 'g'):
			param.gamma = float(sys.argv[i])
		elif(target == 'r'):
			param.coef0 = float(sys.argv[i])
		elif(target == 'n'):
			param.nu = float(sys.argv[i])
		elif(target == 'm'):
			param.cache_size = float(sys.argv[i])
		elif(target == 'c'):
			param.C = float(sys.argv[i])
		elif(target == 'e'):
			param.eps = float(sys.argv[i])
		elif(target == 'p'):
			param.p = float(sys.argv[i])
		elif(target == 'h'):
			param.shrinking = int(sys.argv[i])
		elif(target == 'b'):
			param.probability = int(sys.argv[i])
		elif(target == 'q'):
			param.print_func = PRINT_STRING_FUN(print_null)
		elif(target == 'v'):
			cross_validation = 1
			nr_fold = int(sys.argv[i])
			if(nr_fold < 2):
				print("n-fold cross validation, n must be >= 2\n")
				exit(1)
		elif(target == 'w'):
			param.nr_weight +=1
			param.weight_label.append(int(sys.argv[i-1][2:]))
			param.weight.append(float(sys.argv[i]))
		else:
			print("Unknown option: -%c\n" %sys.argv[i-1][1])
			exit(1)
		i += 1
	libsvm.svm_set_print_string_function(param.print_func)
	if(i >= len(sys.argv)):
		exit(1)
	input_file_name = sys.argv[i]
	model_file_name = None
	if(i < len(sys.argv)-1):
		model_file_name = sys.argv[i+1]
	else:
		p = (sys.argv[i]).rfind('/')
		if(p == -1):
			p = sys.argv[i]
		else:
			p +=1
		model_file_name = str(p) + ".model"
	return(input_file_name, model_file_name)

def read_problem(filename):
	fp = open(filename, "r")

	if(fp == None):
		print("can't open input file %s\n" %filename)
		exit(1)

	prob.l = 0
	elements = 0

	while(fp.readline()):
		myLine = re.split("[ \t]", line)
		p = myLine[0]
		line = line[len(p):]
		while(1):
			myLine = re.split("[ \t]", line)
			p = myLine[0]
			line = line[len(p):]
			if(p == None || p == '\n'):
				break;
			elements += 1
		elements += 1
		prob.l += 1
	fp.seek(0)
	max_index = 0
	j = 0
	for i in range(0, prob.l):
		inst_max_index = -1
		fp.readline()
		prob.append(x_space[j])
		myLine = re.split("[ \t]", line)
		label = myLine[0]
		line = line[len(label):]
		prob.y.append(float(label))
		if(label == None):
			exit_input_error(i+1)
		while(1)
			myLine = re.split("[:]", line)
			idx = myLine[0]
			line = line[len(idx):]
			myLine = re.split("[ \t]", line)
			val = myLine[0]
			line = line[len(val):]

			idx = int(long(idx))
			val = float(val)
			if(val == None || idx == None || errno != 0 || idx <= inst_max_index):
				exit_input_error(i+1)
			else:
				inst_max_index = idx

			x_space.append(svm_node(idx,val))

			j+=1
		if(inst_max_index > max_index):
			max_index = inst_max_index
		x_space[j+=1].index = -1

	if(param.gamma == 0 && max_index > 0):
		param.gamma = 1.0/max_index
	if(param.kernel_type == PRECOMPUTED):
		for i in range(0, prob.l):
			if(prob.x[i][0].index != 0):
				print("Wrong input format: first column must be 0:sample_serial_number\n")
				exit(1)
			if(int(prob.x[i][0].value) <= 0 || int(prob.x[i][0].value) > max_index):
				print("Wrong input format: sample_serial_number out of range\n")
				exit(1)
	fp.close()

def main():
	input_file_name, model_file_name = parse_command_line()
	read_problem(input_file_name)
	error_msg = libsvm.svm_check_parameter(prob, param)
	if(error_msg):
		print("Error: %s\n" %error_msg)
		exit(1)

	if(cross_validation):
		do_cross_validation()
	else:
		model = svm_train(prob, param)
		if(svm_save_model(model_file_name, model)):
			print("can't save model to file %s\n", %model)
			exit(1)
		