import sys
import numpy as np
from io import StringIO

n = 0
d = 0

data = []
thissum = 0
ltwo = 0

filename = sys.argv[1]
print(filename)
print(sys.argv[2])

infile = open(filename, "r")
outfile = open(sys.argv[2], "w")

contents = infile.read()
n = 99420
d = 132

print(str(n) + " " + str(d))

data = [item.split() for item in contents.split('\n')[:-1]]
data = np.asarray(data,dtype=np.single)
infile.close()
print("done")
print(data.shape)

print(data[:,0].size)
for ii in range(0, n):
	temp_matrix = np.array([data[ii],]*n)
	result_matrix = np.subtract(temp_matrix, data)
	result_matrix = np.square(result_matrix)
	thissum += np.sum(result_matrix)
	if (ii%100 == 0):
		print(str(ii))
outfile.write(filename + " " + str(thissum/(n*n)) + "\n")
outfile.close()