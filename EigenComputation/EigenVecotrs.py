from pyariadne import *

def power_methods(A):
    x1 = [1]
    for i in range(A.column_size()-1):
        x1.append(1)
    x1 = FloatDPApproximationVector(x1, dp)
    # x1 = np.array([np.ones(len(A))]).T
    # print("hello",x1)

    for i in range(50):
        x1 = A * x1
        x1 = normalize(x1)
    tmp = A * x1
    l = maxAbsoluteVector(tmp)

    return l, x1

def normalize(x):
    d = maxVector(x)
    x_n = x / d
    return x_n

def maxAbsoluteVector(v):
    maxi = abs(v[0])
    for i in range(1, len(v)):
        maxi = max(abs(v[i]), maxi)
    return maxi

def maxVector(v):
    maxi = v[0]
    for i in range(1, len(v)):
        maxi = max(v[i], maxi)
    return maxi


# A = FloatDPApproximationMatrix([[1, 2, 0],[0, 0, 1],[1, 0, 0]], dp)
#
#
#
# eigenvalues1, eigenvectors1 = power_methods(A)
# print('mine:',eigenvalues1, eigenvectors1)
#
# # v = FloatDPApproximationVector([3,1,1], dp)
# mine: 1.696 [1.000,0.3478,0.5898]
#
#
# # A = np.array([[60, 91, 26], [60, 3, 75], [45, 90, 31]])
# # A = np.array([[1, 2, 0],[0, 0, 1],[1, 0, 0]])
# # A = np.array([[2, -1, 1],[ -1, 3, -2],[1, 2, 3]])
# # A = np.array([[0.9,10.2,0.7],[3.3,0.9,1.2],[0.01,7.4,2.5]])
# # A = np.array([[2, -12], [1, -5]])
# # A = np.array([[2, -12], [1, -5]])
# # A = np.array([[0, 2], [2, 3]])
# # A = np.array([[2, 1], [1,2]])
# print(A)
