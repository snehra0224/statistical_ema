from makesets import *
import sys

SETSIZE = 460
MFCCSIZE = 12

utterance = 1
context = 0
feature = 1
outfilename = "output.dat"

for i in range(1, len(sys.argv)):
	if(sys.argv[i][0] != '-'):
		print("something is wrong, exiting")
		exit(1)
	target = sys.argv[i-1][1]
	if(target == 'f'):
		feature = int(sys.argv[i])
		if(feature<1 || feature>14):
			print("something is wrong, exiting")
			exit(1)
		break
	elif(target == 'u'):
		utterance = int(argv[i])
		if(utterance<0 || utterance>460):
			print("something is wrong, exiting")
			exit(1)
		break
	elif(target == 'c'):
		context = int(argv[i])
		if(context<0):
			print("something is wrong, exiting")
			exit(1)
		break
	elif(target == 'o'):
		outfilename = sys.argv[i]
		break
	else:
		print("Unknown option\n")
		print("something is wrong, exiting")
		exit(1)

infilename = fileNumber2labFileName(utterance)
start_examples_tuple = labName2nonSilentExamples(infilename)
start = start_examples_tuple[0]
examples = start_examples_tuple[1]

thisema = makeema(utterance,start,examples)
thisaudio = makeaudio(utterance, start, examples, context)

fid = open(outfilename,"w")

for i in range(0, examples):
	fid.write("%7.3f\t",thisema[i][feature-1])
	for j in range(0,(2*context+1)*MFCCSIZE):
		fid.write("%i:%7.3f\t", j+1, thisaudio[i][j])
		fid.write("\n")