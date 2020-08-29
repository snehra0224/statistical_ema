from makesets import *
import sys

utterance = 1
for i in range(1, len(sys.argv)):
	if(sys.argv[i][0] != '-'):
		print("Something is wrong, exiting")
		exit(1)
	if(sys.argv[i-1][1] == 'u'):
		utterance = int(sys.argv[i])
		if(utterance < 0 or utterance > 460):
			print("Something is wrong, exiting")
			exit(1)
		break
infilename = fileNumber2labFileName(utterance)
start_examples_tuple = labName2nonSilentExamples(infilename)
print(str(utterance) + ' ' + str(start_examples_tuple[0]) + ' ' + start_examples_tuple[1] + '\n')
