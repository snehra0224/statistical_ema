from makesets import *
import sys

setkind = 0
context = 0
srate = 1
partition = 0
feature = 1
filename = "output.dat"

i = 1
while i < len(sys.argv):
	print("at top i = " + str(i))
	if(sys.argv[i][0] != '-'):
		print("Something is wrong, exiting")
		print("i = " + str(i))
		print("1")
		exit(1)
	i+=1
	target = sys.argv[i-1][1]
	print("target = " + target + " " + sys.argv[i])
	print("when target is acquired i = " + str(i))
	if(target == 'f'):
		feature = int(sys.argv[i])
		if(feature < 1 or feature > 14):
			print("Something is wrong, exiting")
			print("i = " + str(i))
			print("2")
			exit(1)
	elif(target == 'k'):
		setkind = int(sys.argv[i])
		print("in k")
		print("after k, i = " + str(i))
		if(setkind < 0 or setkind > 5):
			print("Something is wrong, exiting")
			print("i = " + str(i))
			print("3")
			exit(1)
	elif(target == 'c'):
		context = int(sys.argv[i])
		if(context < 0):
			print("Something is wrong, exiting")
			print("i = " + str(i))
			print("4")
			exit(1)
	elif(target == 's'):
		srate = int(sys.argv[i])
		if(srate < 0):
			print("Something is wrong, exiting")
			print("i = " + str(i))
			print("5")
			exit(1)
	elif(target == 'o'):
		filename = sys.argv[i]
	elif(target == 'p'):
		partition = int(sys.argv[i])
	else:
		print("Something is wrong, exiting")
		print("i = " + str(i))
		print("6")
		exit(1)
	i+=1

utNumbers = []
if(setkind == 0):
	utNumbers = setSize2trNumbers()
elif(setkind == 1):
	utNumbers = setSize2teNumbers()
elif(setkind == 2):
	utNumbers = setSize2deNumbers()
elif(setkind == 3):
	utNumbers = setSize2trCV(partition)
elif(setkind == 4):
	utNumbers = setSize2teCV(partition)
elif(setkind == 5):
	utNumbers = setSize2alldata()
else:
	print("Something is wrong, exiting")
	print("7")
	exit(1)
start_examples_tuple = numbers2Examples(utNumbers)
utStart = start_examples_tuple[0]
utExamples = start_examples_tuple[1]

fid = open(filename, "w")
totexamples = 0

for i in range(0, SETSIZE):
	totexamples +=utExamples[i]

fid.write("%i %i\n" %(totexamples, (2*context+1)*MFCCSIZE))

dimexamples = 0
utterance = 0

while (utNumbers[utterance]>0):
	for i in range(0, utExamples[utterance], srate):
		dimexamples +=1
	utterance+=1

utterance = 0

while(utNumbers[utterance]>0):
	thisaudio = makeaudio(utNumbers[utterance], utStart[utterance], utExamples[utterance], context)
	for i in range(0, utExamples[utterance], srate):
		for j in range(0, (2*context+1)*MFCCSIZE):
			fid.write("%7.3f\t" %(float(thisaudio[i][j])))
		fid.write("\n")
	utterance+=1
	print("done " + str(utterance))

fid.close()