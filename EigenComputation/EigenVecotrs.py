import numpy as np
import math
from Householder import *

from numpy.linalg import eig
from numpy.linalg import inv


def power_methods(A):
    x1 = np.array([np.ones(len(A))]).T
    # print("hello",x1)

    for i in range(50):
        x1 = np.dot(A, x1)
        print(x1)
        x1 = normalize(x1)
    tmp = np.dot(A, x1)
    l = abs(tmp).max()

    return l, x1

def inversePowerMethod(A, estimate = 1):
    n,m = np.shape(A)
    I = np.identity(n)
    inverseA = inv(A - estimate*I)
    l,x1 = power_methods(inverseA)
    l = np.dot(A,x1)[0]
    print(l)

    return l, x1


def normalize(x):
    newX = x.copy()
    x_n = x / x.max()
    return x_n


def normQR(x):
    x = np.power(x, 2)
    norm = math.sqrt(sum(x))
    return norm


# def qrDecomposition(A):
#     # https://ristohinno.medium.com/qr-decomposition-903e8c61eaab
#     # QR decomposition
#     m, n = A.shape
#     Q = np.zeros((m, n))
#     R = np.zeros((n, n))
#     for i in range(n):
#         v = A[:, i]
#         for j in range(i - 1):
#             q = Q[:, j]  # This q value is not 0 anymore, has been
#             R[j, i] = np.dot(q, v)
#             v = v - R[j, i] * q
#         norm = normQR(v)
#         print(norm)
#         Q[:, i] = v / norm
#         R[i, i] = norm
#         print('hello')
#     return Q, R


# A = np.array([[60, 91, 26], [60, 3, 75], [45, 90, 31]])
A = np.array([[1, 2, 0],[0, 0, 1],[1, 0, 0]])
# A = np.array([[2, -1, 1],[ -1, 3, -2],[1, 2, 3]])
# A = np.array([[2, -12], [1, -5]])
# A = np.array([[2, -12], [1, -5]])
# A = np.array([[0, 2], [2, 3]])
# A = np.array([[2, 1], [1,2]])
print(A)

# eigenvalues, eigenvectors = eig(A)
eigenvalues1, eigenvectors1 = power_methods(A)
# eigenvalues2, eigenvectors2 = inversePowerMethod(A, 1.5)
# print(eigenvalues, eigenvectors[1])
print('mine:',eigenvalues1, eigenvectors1)
# print('mine', eigenvalues2, eigenvectors2)

# print(A.dot(eigenvectors[:,1]))
print('aaa',A.dot(eigenvectors1))
print('aaa',eigenvalues1*eigenvectors1)
# print('bbb',np.dot(A,eigenvectors2))
# print('bbb',eigenvalues2*eigenvectors2)

# eigenVal, eigenVect = findEigen(A)
# print(eigenVal)
# print(eigenVect)







# from pyariadne import *
#
#
# def power_methods(A):
#     x1 = [1]
#     for i in range(A.column_size()-1):
#         x1.append(1)
#     x1 = FloatDPApproximationVector(x1, dp)
#     # x1 = np.array([np.ones(len(A))]).T
#     # print("hello",x1)
#
#     for i in range(50):
#         x1 = A * x1
#         x1 = normalize(x1)
#     tmp = A * x1
#     l = maxAbsoluteVector(tmp)
#
#     return l, x1
#
# def normalize(x):
#     d = maxVector(x)
#     x_n = x / d
#     return x_n
#
# def maxAbsoluteVector(v):
#     maxi = abs(v[0])
#     for i in range(1, len(v)):
#         maxi = max(abs(v[i]), maxi)
#     return maxi
#
# def maxVector(v):
#     maxi = v[0]
#     for i in range(1, len(v)):
#         maxi = max(v[i], maxi)
#     return maxi
#
#
# A = FloatDPApproximationMatrix([[1, 2, 0],[0, 0, 1],[1, 0, 0]], dp)
#
#
# eigenvalues1, eigenvectors1 = power_methods(A)
# print('mine:',eigenvalues1, eigenvectors1)
#
# # v = FloatDPApproximationVector([3,1,1], dp)
# mine: 1.696 [1.000,0.3478,0.5898]