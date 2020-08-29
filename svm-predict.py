from svmutil import *
from commonutil import *
from svm import *
import sys
import os
import re

node_array = []
max_nr_attr = 64
model = None
predict_probability = 0

def svm_predict_probability(model_, node_array_, prob_estimates):
	c_prob_estimates = (c_double * len(prob_estimates))()
	for i in range(0, len(prob_estimates)):
		c_prob_estimates[i] = prob_estimates[i]
	return libsvm.svm_predict_probability(model, node_array_, c_prob_estimates)

def exit_input_error(line_num):
	print("Wrong input formate at line %d\n", %line_num)
	exit(1)

def predict(_input, _output):
	correct = 0
	total = 0
	error = 0
	sump = 0
	sumt = 0
	sumpp = 0
	sumtt = 0
	sumpt = 0

	infile = open(_input, "r")
	outfile = open(_output, "w")

	svm_type = model.get_svm_type()
	nr_class = model.get_nr_class()
	prob_estimates = []
	if(predict_probability):
		if(svm_type==NU_SVR || svm_type==EPSILON_SVR):
			print("Prob. model for test data: target value = predicted value + z,\nz: Laplace distribution e^(-|z|/sigma)/(2sigma),sigma=%g\n",model.get_svr_probability())
		else:
			labels = model.get_labels()
			for j in range(0, nr_class):
				outfile.write(" %d" %labels[j])
			outfile.write("\n")

	line = infile.readline()
	while line:
		i = 0
		inst_max_index = -1
		myLine = re.split("[ \t]", line)
		label = myLine[0]
		line = line[len(label):]
		target_label = float(label)
		if(label == None):
			exit_input_error(total+1)
		while(1):
			if(i>=max_nr_attr-1):
				max_nr_attr *= 2
			myLine = re.split("[:]", line)
			idx = myLine[0]
			line = line[len(idx):]
			myLine = re.split("[ \t]", line)
			val = myLine[0]
			line = line[len(val):]

			if(val == None)
				break
			errno = 0
			idx = int(long(idx))
			val = float(val)
			if(val == None || idx == None || errno != 0 || idx <= inst_max_index):
				exit_input_error(total+1)
			else:
				inst_max_index = idx
			node_array.append(svm_node(idx, val))

			i+=1
		node_array[i].index = -1

		if(predict_probability && (svm_type==C_SVC || svm_type==NU_SVC)):
			predict_label = svm_predict_probability(model, node_array, prob_estimates)
			outfile.write("%g" %predict_label)
			for j in range(0, nr_class):
				outfile.write(" %g" %prob_estimates[j])
			outfile.write("\n")
		else:
			predict_label = libsvm.svm_predict(model, node_array)
			outfile.write("%g\n", predict_label)
		if(predict_label == target_label)
			correct += 1
			error += (predict_label - target_label)**2
			sump += predict_label
			sumt += target_label
			sumpp += predict_label**2
			sumtt += target_label**2
			sumpt += predict_label * target_label
			total += 1
		line = infile.readline()

	if(svm_type==NU_SVR || svm_type==EPSILON_SVR):
		print("Mean squared error = %g (regression)\n" %error/total)
		print("Squared correlation coefficient = %g (regression)\n" %(((total*sumpt-sump*sumt)**2)/((total*sumpp-sump*sump)*(total*sumtt-sumt*sumt))))
	else:
		print("Accuracy = %g%% (%d/%d) (classification)\n" %(double(correct/total*100), correct, total))
	infile.close()
	outfile.close()

def main():
	for i in range(1, len(sys.argv)):
		if(sys.argv[i][0] != '-'):
			break
		i += 1
		target = sys.argv[i-1][1]
		if(target == 'b'):
			predict_probability = int(sys.argv[i])
			break
		else:
			print("Unknown option: -%c\n", %sys.argv[i-1][1])
			exit(1)
	if(i>=2):
		exit(1)
	input_ = sys.argv[i]
	if(open(input) == None):
		print("can't open input file")
	output = sys.argv[i+2]
	if(open(output) == None):
		print("can't open output file")
	model = svm_load_model(sys.argv[i+1])
	if(predict_probability):
		if(!model.is_probability_model()):
			print("model does not support probability estimates\n")
			exit(1)
	else:
		if(model.is_probability_model()):
			print("Model supports probability estimates, but disabled in prediction\n")
	predict(input_, output)

if __name__=='__main__':
	main()