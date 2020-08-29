from makesets import *
import sys

utterance = 1
LABSIZE = 10

if(len(sys.argv) != 2):
	print("Something is wrong, exiting\n")
	exit(1)

utterance = int(sys.argv[1])

infilename = fileNumber2labFileName(utterance)
start_nsexamples_tuple = labName2nonSilentExamples(infilename)
start = start_nsexamples_tuple[0]
nsexamples = start_nsexamples_tuple[1]

f = open(infilename)
if(!f):
	print("File could not be opened\n")
	print(infilename)
	exit(1)
allexamples = 0
contents = f.read().split()
allexamples = contents[0]
contents.pop(0)
labels = []
for i in range(0, allexamples):
	labels.append(contents[i])
output_string = ""
for i in range(start,start+nsexamples):
	output = output + labels[i] + " "
output = output + "\n"
print(output)