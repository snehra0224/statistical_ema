from makesets import *
import sys

SETSIZE = 460
MFCCSIZE = 12

setkind = 0
context = 0
srate = 1
partition = 0
feature = 1
filename = "output.dat"

for i in range(1,len(sys.argv)):
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
	elif(target == 'k'):
		setkind = int(sys.argv[i])
		if(setkind<0 ||setkin>4):
			print("something is wrong, exiting")
			exit(1)
		break
	elif(target == 'c'):
		context = int(sys.argv[i])
		if(context<0):
			print("something is wrong, exiting")
			exit(1)
		break
	elif(target == 's'):
		srate = int(sys.argv[i])
		if(srate<0):
			print("something is wrong, exiting")
			exit(1)
		break
	elif(target == 'o'):
		filename = sys.argv[i]
		break
	elif(target == 'p'):
		partition = int(sys.argv[i])
		break
	else:
		print("Unknown option\n")
		print("something is wrong, exiting")
		exit(1)
utNumbers = []
if(setkind == 0):
	utNumbers = setSize2trNumbers()
	break
elif(setkind == 1):
	utNumbers = setSize2teNumbers()
	break
elif(setkind == 2):
	utNumbers = setSize2deNumbers()
	break
elif(setkind == 3):
	utNumbers = setSize2trCV(partition)
	break
elif(setkind == 4):
	utNumbers = setSize2teCV(partition)
	break
else:
	print("something is wrong, exiting")
	exit(1)
utStart = []
utExamples = []
numbers2Examples(utNumbers,utExamples,utStart)
fid = open(filename, "a")
totalexamples = 0
for i in range(0,SETSIZE):
	totalexamples +=utExamples[i]
dimexamples = 0
utterance = 0
while utNumbers[utterance] > 0:
	for i in range(0, utExamples[utterance], srate):
		dimexamples+=1
	utterance += 1
utterance = 0
thisema = [[]]
thisaudio = [[]]
while utNumbers[utterance] > 0:
	thisema = makeema(utNumbers[utterance],thisema,utStart[utterance],utExamples[utterance])
	thisaudio = makeaudiolipjaw(utNumbers[utterance],thisaudio,utStart[utterance],utExamples[utterance], context)
	for i in range(0,utExamples[utterance],srate):
		fid.write("%7.3f\t",thisema[i][feature-1])
		for j in range(0,(2*context+1)*MFCCSIZE):
			fid.write("%i:%7.3f\t",j+1,thisaudio[i][j])
		fid.write("\n")
	utterance+=1