import numpy as np

data = np.array(([1,2,3],[4,5,6]))
print(data)
print(data[:,0])
data2 = np.array([data[1],]*3).transpose()
print(data2)
