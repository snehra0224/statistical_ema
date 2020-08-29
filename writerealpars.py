from makesets import *
import sys

utterance = 1
outfilename = "output.dat"

for i in range(1, len(sys.argv)):
	if(sys.argv[i][0] != '-'):
		print("something is wrong, exiting")
		exit(1)
	target = sys.argv[i-1][1]
	if(target == 'u'):
		utterance = int(sys.argv[i])
		if(utterance < 0 || utterance > 460):
			print("something is wrong, exiting")
			exit(1)
	elif(target == 'o'):
		outfilename = sys.argv[i]
	else:
		print("something is wrong, exiting")
		exit(1)

infilename = fileNumber2labFileName(utterance)
start_examples_tuple = labName2nonSilentExamples(infilename)
start = start_examples_tuple[0]
examples = start_examples_tuple[1]

thispar = makepars(utterance, start, examples)

fid = open(outfilename, "w")

for i in range(0, examples):
	for j in range(0, EMASIZE):
		fid.write("%7.3f\t",thisema[i][j])
		fid.write("\n")

