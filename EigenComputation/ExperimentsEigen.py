from pyariadne import *
import numpy as np
import time
import Householder

# FloatDPApproximation(16*log(10)/log(2),dp)

times = []
for i in range(1,10):
    a = np.random.rand(i*10,i*10)
    print(i)
    A = FloatDPApproximationMatrix(a.tolist(), dp)
    A = A * transpose(A)
    startTime = time.time()
    Householder.findEigenAriadne(A)
    endtime = time.time()
    times.append(endtime - startTime)

print(times)

# [1.4193274974822998, 12.05971646308899, 34.601951599121094, 80.84929299354553, 160.0817515850067, 289.89614725112915, 530.9115586280823, 844.7288746833801, 1090.6577203273773]