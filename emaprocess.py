import numpy as np
import math

def ema_process(this_set):
	stats_tuple = find_stats(this_set)
	baraudio = stats_tuple[0]
	backaudio = stats_tuple[1]
	barema = stats_tuple[2]
	backema = stats_tuple[3]
	arr = numpy.array(baraudio, backaudio, barema, backema)
	np.save(normalema, arr)

	smoothmeans=get_means(this_set)

	for i in this_set:
		mocha2mat_tuple = mocha2mat(i)
		audio = mocha2mat_tuple[0]
		ema = np.array(mocha2mat_tuple[1])
		labels = mocha2mat_tuple[2]

		audio = centering(audio, baraudio)
		audio = scaling(audio, backaudio)

		ema = ema - np.ones((ema.shape)[0],1)*smoothmeans[i]
		ema = centering(ema, barema)
		ema = scaling(ema, backema)
		fileaudio = './processedData/mfcc/mfcc_%03d.txt' % {i}
		fileema = './processedData/ema/ema_%03d.txt' % {i}
		filelabels = './processedData/labels/labels_%03d.txt' % {i}
		mat2file(audio, fileaudio)
		mat2file(ema, fileema)
		lab2file(labels, filelabels)

def mocha2mat(utterance):
	filestr = './mocha/mfccfiles/fsew0_%03d.mfc' % {utterance}
	audio = np.array(htkread(filestr))
	filestr = './mocha/emafiles/fsew0_%03d.ema' % {utterance}
	emadata = numpy.array(readest(filestr, 'r', -1, 6))
	channels = [2, 7, 3, 8, 4, 9, 5, 10, 11, 16, 12, 17, 13, 18]
	ema  = emadata[:,channels]

	labfile = './mocha/labfiles/fsew0_%03d.lab' % utterance
	f = open(labfile, 'r')
	arr = np.loadtxt(f, dtype{'formats':('f4', 'f4', 'S1')})
	starttime = []
	endtime = []
	label = []
	label_vector = np.zeros(floor(((ema.shape)[0])/5))
	for i in arr:
		starttime.append(i[0])
		endtime.append(i[1])
		label.append(i[2])
	for i in range (0, floor(((ema.shape)[0])/5)):
		time = i/100
		for j in range(0, len(label)):
			starttimej = starttime[j] - 0.0125
			endtimej = endtime(j) - 0.0125

			if((time >= starttimej) && (time<endtimej)):
				label_vector[i] = label[j]


	for i in range(0, 14):
		ema[:,i] = ema_filter(ema[:,i], 20, 500)

	ema = ema(1:5:end,:)

	minsize = min([(audio.shape)[0], (ema.shape)[0], len(label_vector)])
	audio = audio[1:minsize,:]
	ema_vector = ema(1:minsize, :)/100
	label_vector = np.transpose(label_vector[1:minsize])

	return (audio, ema_vector, label_vector)

def find_stats(this_set):
	setsize = 0
	oldsize = 0
	ema_means = np.zeros(460,14)

	for i in this_set:
		mocha2mat_tuple = mocha2mat(i)
		audio = mocha2mat_tuple[0]
		ema = mocha2mat_tuple[1]
		labels = mocha2mat_tuple[2]

		setsize = setsize+(audio.shape)[0]

	smoothmeans = get_means(this_set)
	fullaudio = np.zeros(setsize, (audio.shape)[1])
	fullema = np.zeros(setsize, (audio.shape)[1])

	for i in this_set:
		mocha2mat_tuple = mocha2mat(i)
		audio = mocha2mat_tuple[0]
		ema = np.array(mocha2mat_tuple[1])
		labels = mocha2mat_tuple[2]

		ema = ema - np.ones((ema.shape)[0],1)*smoothmeans[i]
		newsize = oldsize+(audio.shape)[0]
		audio = fullaudio[oldsize+1 : newsize]
		ema = fullema(oldsize+1 : newsize)
		oldsize = newsize

	baraudio = (centering(fullaudio))[1]
	backaudio = (scaling(fullaudio))[1]
	barema = (centering(fullaudio))[1]
	backema = (scaling(fullaudio))[1]

	return (baraudio, backaudio, barema, backema)

def centering(DATA, barX):
	DATA = numpy.array(DATA)
	barX = mean((DATA.shape)[0])

	for i in range(0, (DATA.shape)[1]):
		DATA[:, i] = DATA[:, i] - barX(i)

	return (DATA, barX)

def scaling(DATA, backmap):
	DATA = numpy.array(DATA)
	k = (DATA.shape)[0]
	n = (DATA.shape)[1]

	if(n > k):
		print("Data matrix should be transposed?")
	R = np.multiply(DATA.transpose(), (DATA/k))

	backmap = np.diag(np.sqrt(np.diag(R)))

	backmap1 = np.diag(backmap)

	for i in range(0, (DATA.shape[1])):
		DATA[:,i] = np.true_divide(DATA[:,i], backmap1(i))

def get_means(this_set):
	rawMeans = np.zeros(460,14)
	smoothmeans = np.zeros(460,14)

	for i in range(0, len(this_set)):
		mocha2mat_tuple = mocha2mat(utterance)
		audio = mocha2mat_tuple[0]
		ema = mocha2mat_tuple[1]
		labels = mocha2mat_tuple[2]

		rawMeans[i] = mean(ema)
	for j in range(0,14):
		
def mov_avg(X, points):
	n = len(X)
	d = len(X[0])
	Y = np.zeros(n,d)

	for i in range(0, n):
		tmpsum = np.zeros(d)
		for j in range(i-points, i+points):
			if(j < 1):
				tmpsum = tmpsum+X[1:]
			elif (j > n):
				tmpsum = tmpsum+X[n:]
			else:
				tmpsum = tmpsum+X[j:]
		Y[i:]=tmpsum/(2*points+1)

	return Y

def ema_filter(x, cutoff, Fs):
	x = x.getH() #complex conjugate transpose of x
	mu = x.mean()
	sigma = x.std()
	x = (x-mu)/sigma #z-score

	M = len(x)

	L = 257
	fc = cutoff

	hsupp  =(-(L-1)/2:(L-1)/2)
	hideal = (2*fc/Fs)*np.sinc((2*fc*hsupp)/Fs)
	h = np.multiply((np.hamming(L).getH()), hideal)

	absval = abs(L+M-1)
	Nfft = 2**(ceil(math.log(absval,2)))

	numx = np.array(x)
	xzp = np.concatenate(numx, np.zeros(Nfft-M))
	numh = np.array(h)
	hzp = np.concatenate(numh, np.zeros(Nfft-L))

	X = np.fft.fft(xzp)
	H = np.fft.fft(hzp)

	Y = np.multiply(X, H)
	y = np.fft.ifft(Y)
	y = np.array(y)
	y = np.real(y)
	y = y((L-1)/2+1:(L-1)/2+M)
	y = y.getH()
	y = y*sigma+mu

	return y

def mat2file(DATA, filename):
	examples = len(DATA)
	dimensionality = len(DATA[0])
	fid = open(filename, "w")
	fid.write("%d %d\n" % {examples, dimensionality})
	for i in range(0, examples):
		for j in range(0, dimensionality):
			fid.write("%8.3f\t", DATA[i][j])
		fid.write("s\n")
	fid.close()

def lab2file(DATA, filename):
	if(len(DATA) > len(DATA[0])):
		examples = len(DATA)
	else:
		examples = len(DATA[0])
	fid = open(filename, "w")
	examples_str = str(examples)
	fid.write(examples_str)
	fid.write('\n')
	for i in range(0, examples):
		fid.write(DATA[i])
	fid.close()
