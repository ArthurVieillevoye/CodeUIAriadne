import numpy as np
import json
from numpy.linalg import inv
from numpy.linalg import eig

def power_methods(A):
    x1 = np.array([np.ones(len(A))]).T
    # print("hello",x1)

    for i in range(5):
        x1 = np.dot(A, x1)
        # print(x1)
        l, x1 = normalize(x1)
        print(l)

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
    factor = abs(newX).max()
    # print("       ", x.max())
    x_n = x / x.max()
    # print('x_n: ', x_n)
    # print("------------------")
    return factor, x_n

# a = np.array([[1, 2], [3, 4]])
# b = np.array([[5, 6], [7, 8]])
# c = np.array([[9, 10], [11, 12]])
A = np.array([[2, -1, 1],[ -1, 3, -2],[1, 2, 3]])

eigenvalues2, eigenvectors2 = inversePowerMethod(A, 3)
eigenvalues, eigenvectors = eig(A)
print(eigenvalues)

print('--------------')
print('bbb',np.dot(A,eigenvectors2))
print('bbb',eigenvalues2*eigenvectors2)