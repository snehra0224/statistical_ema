
SETSIZE=460
EMASIZE=14
MFCCSIZE=12
LABSIZE=10
PARSIZE=7

def makeaudio(fileNo,start,examples,context):
	filename = fileNumber2audioFileName(fileNo)
	audionocontext = readData(filename)
	audiocontext = []
	for i in range(0, examples):
		temp = []
		for j in range(0,(2*context+1)*MFCCSIZE):
			temp.append(0)
		audiocontext.append(temp)

	ii = 0
	for i in range(start,start+examples):
		for jj in range(0, MFCCSIZE):
			for k in range(-context,context+1):
				audiocontext[ii][jj+MFCCSIZE*(context+k)]=audionocontext[i-k][jj]
		ii+=1

	data = []
	for i in range(0, examples):
		temp = []
		for j in range(0,(2*context+1)*MFCCSIZE):
			temp.append(0)
		data.append(temp)

	for i in range(0, examples):
		for j in range(0,(2*context+1)*MFCCSIZE):
			data[i][j] = audiocontext[i][j]
	return data

def makeema(fileNo, start, examples):
	filename = fileNumber2emaFileName(fileNo)
	emaold = readData(filename)
	emanew = []
	for i in range(0, examples):
		temp = []
		for j in range(0, EMASIZE):
			temp.append(0)
		emanew.append(temp)

	ii = 0
	for i in range(start, start+examples):
		for j in range(0, EMASIZE):
			emanew[ii][j] = emaold[i][j]
		ii+=1

	data = []
	for i in range(0, examples):
		temp = []
		for j in range(0, EMASIZE):
			temp.append(0)
		data.append(temp)

	for i in range(0, examples):
		for j in range(0, EMASIZE):
			data[i][j] = emanew[i][j]
	return data

def makejustlipjaw(fileNo,start, examples, context):
	filename = fileNumber2emaFileName(fileNo)
	ema = readData(filename)

	justlipjaw = []
	for i in range(0, examples):
		temp = []
		for j in range(0, (2*context+1)*6):
			temp.append(0)
		justlipjaw.append(temp)

	ii = 0

	for i in range(start, start+examples):
		for jj in range (0, 6):
			for k in range(-context, context+1):
				justlipjaw[ii][jj+6*(context+k)] = ema[i-k][jj]
		ii+=1

	data = []
	for i in range(0, examples):
		temp = []
		for j in range(0,(2*context+1)*6):
			temp.append(0)
		data.append(temp)

	for i in range(0, examples):
		for j in range(0, (2*context+1)*6):
			data[i][j]=justlipjaw[i][j]
	return data

def makeaudiolipjaw(fileNo, start, examples, context):
	filename = fileNumber2audioFileName(fileNo)
	audio = readData(filename)

	fileName = fileNumber2emaFileName(fileNo)
	ema = readData(filename)

	audiolipjaw = []
	for i in range(0, examples):
		temp = []
		for j in range(0, (2*context+1)*(MFCCSIZE+6)):
			temp.append(0)
		audiolipjaw.append(temp)

	ii = 0

	for i in range(start, start+examples):
		for jj in range(0, MFCCSIZE):
			for k in range(-context, context+1):
				audiolipjaw[ii][jj+(MFCCSIZE+6)*(context+k)] = audio[i-k][jj]
		for jj in range(MFCCSIZE, MFCCSIZE+6):
			for k in range(-context,context+1):
				audiolipjaw[ii][jj+(MFCCSIZE+6)*(context+k)] = ema[i-k][jj-MFCCSIZE]
		ii+=1

	data = []
	for i in range(0, examples):
		temp = []
		for j in range(0, (2*context+1)*(MFCCSIZE+6)):
			temp.append(0)
		data.append(temp)
	for i in range(0, examples):
		for j in range(0, (2*context+1)*(MFCCSIZE+6)):
			data[i][j] = audiolipjaw[i][j]

	return data

def makepars(fileNo, start, examples):
	thissum = 0
	ema = makeema(fileNo, start, examples)
	U = readUtable
	stdpca = readstdpar
	stdema = readstdema

	pars = []
	for i in range(0, examples):
		temp = []
		for j in range(0, PARSIZE):
			temp.append(0)
		pars.append(temp)

	for i in range(0, examples):
		for j in range(0, PARSIZE):
			thissum = 0
			for k in range(0, EMASIZE):
				thissum += (stdema[k]*ema[i][k])*U[k][j]
			pars[i][j] = thissum/stdpca[j]
	return pars

def numbers2Examples(Numbers):
	Examples = []
	Start = []
	for i in range(0, SETSIZE):
		Examples.append(0)
		Start.append(0)

	i = 0
	while Numbers[i] > 0:
		filename = fileNumber2labFileName(Numbers[i])
		# print("filename = " + filename)
		start, examples = labName2nonSilentExamples(filename)
		Examples[i] = examples
		Start[i] = start
		i+=1
	return(Start, Examples)

def setSize2alldata():
	allNumbers = []
	for i in range(0, SETSIZE):
		allNumbers.append(i+1)
	return allNumbers

def setSize2trNumbers():
	trNumbers = []
	for i in range(0, SETSIZE):
		trNumbers.append(0)
	i = 0
	for j in range(1, SETSIZE+1):
		if((j%10!=2) and (j%10!=6)):
			trNumbers[i] = j
			i+=1
	return trNumbers

def setSize2teNumbers():
	teNumbers = []
	for i in range(0, SETSIZE):
		teNumbers.append(0)
	i = 0
	for j in range(1, SETSIZE+1):
		if(j%10==6):
			teNumbers[i]=j
			i+=1
	return teNumbers

def setSize2deNumbers():
	deNumbers = []
	for i in range(0, SETSIZE):
		deNumbers.append(0)
	i = 0
	for j in range(1, SETSIZE+1):
		if(j%10==2):
			deNumbers[i]=j
			i+=1
	return deNumbers

def setSize2trCV(partition):
	trNumbers = []
	for i in range(0, SETSIZE):
		trNumbers.append(0)
	i = 0
	for j in range(1,SETSIZE+1):
		if(j%5!=partition):
			trNumbers[i]=j
			i+=1
	return trNumbers

def setSize2teCV(partition):
	teNumbers = []
	for i in range(0, SETSIZE):
		teNumbers.append(0)
	i = 0
	for j in range(1, SETSIZE+1):
		if(j%5==partition):
			teNumbers[i] = j
			i+=1
	return teNumbers

def fileNumber2labFileName(fileNumber):
	strNo = str(fileNumber)
	dispNo = ""
	if(fileNumber < 10):
		dispNo = "00"+strNo
	elif(fileNumber < 100):
		dispNo = "0"+strNo
	else:
		dispNo = strNo

	labfile = "../processedData/labels/labels_" + dispNo + ".txt"
	return labfile

def fileNumber2emaFileName(fileNumber):
	strNo = str(fileNumber)
	dispNo = ""
	if(fileNumber < 10):
		dispNo = "00"+strNo
	elif(fileNumber < 100):
		dispNo = "0"+strNo
	else:
		dispNo = strNo

	emafile = "../processedData/ema/ema_" + dispNo + ".txt"
	return emafile

def fileNumber2audioFileName(fileNumber):
	strNo = str(fileNumber)
	dispNo = ""
	if(fileNumber < 10):
		dispNo = "00"+strNo
	elif(fileNumber < 100):
		dispNo = "0"+strNo
	else:
		dispNo = strNo

	audiofile = "../processedData/mfcc/mfcc_" + dispNo + ".txt"
	return audiofile

def labName2nonSilentExamples(file):
	examples = 0
	nonsilexamples = 0
	befsilexamples = 0

	f = open(file)

	# if(!f):
	# 	print(file + " could not be opened\n")
	# 	exit(1)
	content = f.read().split()
	examples = int(content[0])
	content.pop(0)
	labels = []
	for i in range(0, examples):
		labels.append(content[i])

	f.close()

	i = 0
	while(((len(labels[i]) > 1) and (((labels[i][0]=='s') and (labels[i][1]=='i')) or ((labels[i][0]=='b') and(labels[i][1]=='r'))))==1):
		# print ("befsile labels index = " + str(i))
		# print(labels[i])
		befsilexamples+=1
		i+=1
	for p in range(0, examples):
		if(len(labels[p]) < 2):
			# print ("nonsile labels index = " + str(p))
			# print(labels[p])
			nonsilexamples+=1
		elif ((((labels[p][0]=='s') and (labels[p][1]=='i')) or ((labels[p][0]=='b') and (labels[p][1]=='r')))==0):
			# print ("nonsile labels index = " + str(p))
			# print(labels[p])
			nonsilexamples+=1

	start = befsilexamples
	number = nonsilexamples
	return (start, number)

def readData(file):
	f = open(file)
	# if(!f):
	# 	print(file + " could not be opened\n")
	# 	exit(1)
	contents = f.read().split()
	examples = int(contents[0])
	dimensionality = int(contents[1])
	contents.pop(0)
	contents.pop(0)
	data = []
	for i in range(0, examples):
		temp = []
		for j in range(0, dimensionality):
			temp.append(contents[0])
			contents.pop(0)
		data.append(temp)
	f.close()
	return data

def readUtable():
	infile = open("../model/Utable.txt")
	# if(!infile):
	# 	print("Utable file could not be opened/n")
	# 	exit(1)
	contents = infile.read().split()

	U = []
	for i in range(0, EMASIZE):
		temp = []
		for j in range(0, PARSIZE):
			temp.append(contents[0])
			contents.pop(0)
		U.append(temp)
	return U

def readstdpar():
	infile = open("../model/stdpar.txt")
	# if(!infile):
	# 	print("stdpar file could not be opened\n")
	# 	exit(1)
	contents = infile.read().split()

	stdpar = []
	for i in range(0, PARSIZE):
		stdpar.append(contents[0])
		contents.pop(0)
	return stdpar

def readbarema():
	infile = open("../model/barema.txt")
	# if(!infile):
	# 	print("barema file could not be opened\n")
	# 	exit(1)
	contents = infile.read().split()

	barema = []
	for i in range(0, EMASIZE):
		barema.append(contents[0])
		contents.pop(0)
	return barema

def readstdema():
	infile = open("../model/stdema.txt")
	# if(!infile):
	# 	print("stdema file could not be opened")
	# 	exit(1)
	contents = infile.read().split()

	stdema = []
	for i in range(0, EMASIZE):
		stdema.append(contents[0])
		contents.pop(0)

