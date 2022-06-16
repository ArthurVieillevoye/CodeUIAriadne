from pyariadne import *
import numpy as np
import time
import Householder
import IntervalNewtonMethod
# import matplotlib.pyplot as plt


# FloatDPApproximation(16*log(10)/log(2),dp)

# times = []
# for i in range(1,10):
#     a = np.random.rand(i*10,i*10)
#     print(i)
#     pr = precision(128)
#     A = FloatMPApproximationMatrix(a.tolist(), pr)
#     A = A * transpose(A)
#     startTime = time.time()
#     Householder.findEigenAriadne(A)
#     endtime = time.time()
#     times.append(endtime - startTime)
#
# print(times)

# On1 = []
# On2 = []
# On3 = []
# On4 = []
#
# for i in range(1,10):
#      On1.append(i*10)
#      On2.append((i*10)**2)
#      On3.append((i * 10)** 3)
#      On4.append((i*10)**4)
#
# a = [1.4193274974822998, 12.05971646308899, 34.601951599121094, 80.84929299354553, 160.0817515850067, 289.89614725112915,
#      530.9115586280823, 844.7288746833801, 1090.6577203273773]
#
# tmp1 = On1[0]
# tmp2 = On2[0]
# tmp3 = On3[0]
# tmpexp = On4[0]
# other = []
# for i in range(len(On1)):
#      On1[i] = ((On1[i] / tmp1) * a[0])
#      On2[i] = ((On2[i] / tmp2) * a[0])
#      On3[i] = ((On3[i] / tmp3) * a[0])
#      On4[i] = ((On4[i] / tmpexp) * a[0])
#
# i = [10,20,30,40,50,60,70,80,90]
# print(len(i), len(a))
#
# plt.plot(i,a,'r--', label="Time of INM" )
# plt.plot(i,On1, 'b', label="O(n)")
# plt.plot(i, On2,'g', label="O(n²)")
# plt.plot(i, On3,'m', label="O(n³)")
# # plt.plot(i, On4,'c', label="O(n⁴)")
# plt.title("Time complexity of Interval Newton Method for symmetric matrices")
# plt.xlabel('Size of the matrix (nXn)')
# plt.ylabel('Time(s)')
# plt.legend()
# plt.show()



def average(list):
    avg = []
    for i in range(len(list[0])):
        nb2 =0
        nb1 = 0
        nb0 = 0
        for j in range(len(list)):
            if list[j][i] == 2:
                nb2 +=1
            elif list[j][i] == 1:
                nb1 +=1
            elif list[j][i] == 0:
                nb0 = 0
        avg.append((nb0,nb1,nb2))
    return avg
#
#
# results = []

# A = FloatMPApproximationMatrix([[52, 30, 49, 28], [30, 50, 8, 44], [49, 8, 46, 16], [28, 44, 16, 22]], precision(128))
# # A = FloatMPApproximationMatrix([[10, -1, 1], [-1, 30, 2], [1, 2, 20]], precision(128))

#times = []
# for i in range(1,50):
#     a = np.random.rand(3,3)
#     print(i)
#     pr = precision(128)
#     A = FloatMPApproximationMatrix(a.tolist(), pr)
#     A = A * transpose(A)
#     eigenval, eigenvect = Householder.findEigenAriadne(A)
#     lamb = eigenval[0]
#     v = eigenvect[0]
#     tmp = []
#     for j in range(50):
#         tmp.append(IntervalNewtonMethod.intervalNewtonMethods(v,lamb,A,j))
#     times.append(tmp)
# print(times[0])
# A = FloatMPApproximationMatrix([[12,-51,14,11], [16,167,-68,11], [-14,24,-41,11], [-4,24,-41,11]], precision(128))
A = FloatMPApproximationMatrix([[52, 30, 49, 28], [30, 50, 8, 44], [49, 8, 46, 16], [28, 44, 16, 22]], precision(128))
steps = []
for i in range(1,21):
    precision = 1/(10**i)
    print(precision)
    a, b, counter = Householder.findEigenAriadne(A, precision)
    steps.append((counter, np.array([eval(str(A*b[0] - a[0]*b[0]))])))
    print("hello")
    print(i, precision)

print(steps)
# [7, 9, 12, 14, 17, 19, 22, 24, 27, 29, 32, 34, 37, 39, 42, 44, 47, 49, 52, 54]


# [(0, 0, 50), (0, 0, 50), (0, 0, 50),(0, 0, 50),(0, 0, 50), (0, 0, 50), (0, 0, 50), (0, 0, 50), (0, 0, 50), (0, 0, 50),
# (0, 0, 50), (0, 0, 50), (0, 0, 50), (0, 0, 50), (0, 0, 50), (0, 0, 50), (0, 0, 50), (0, 0, 50), (0, 0, 50),v(0, 0, 50),
# (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),(0, 0, 0),
# (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
# (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
