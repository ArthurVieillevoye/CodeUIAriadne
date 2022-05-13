from Householder import findEigen
import numpy as np


def F0(A, v, l):
    return np.dot(A, v) - (l * v)


def F1(v):
    return 1 - np.dot(v, v.T)


def f0l(v):
    if v.shape[1] == 1:
        return -v
    else:
        return -v.T


def f0v(l, A):
    I = np.identity(A.shape[0])
    return A - l * I


def f1v(v):
    if v.shape[0] == 1:
        return -v
    else:
        return -v.T


def newtonMethods(x, eps=2 ** (-23)):
    topBoundFound = False
    lowBoundFound = False
    xTop = x + 2 ** (-10)
    xLow = x - 2 ** (-10)
    # print(xTop)
    # print(xLow)

    while not topBoundFound and not lowBoundFound:
        xTop_val = F1(xTop.T)
        # print(xTop_val)
        xLow_val = F1(xLow.T)
        topBound = []
        lowBound = []

        if np.isnan(np.sum(xTop)):
            break

        elif abs(xTop_val).all() < eps and not topBoundFound:
            topBound = xTop
            print('hello1')
            topBoundFound = True
        elif abs(xLow_val).all() < eps and not lowBoundFound:
            lowBound = xLow
            print('hello2')
            lowBoundFound = True
        else:
            if not topBoundFound:
                xTop = updateVector(xTop, xTop_val)
                print(xTop)
            elif not lowBoundFound:
                xLow = updateVector(xLow, xLow_val)


        # lowBoundFound = True
        # topBoundFound = True

    return topBound, lowBound


def updateVector(x, Fx):
    print(x)
    fx = f1v(x)
    print(Fx)
    print(fx)
    difference = Fx / fx
    print(difference)
    if difference.shape[0] == 1:
        return x - difference.T
    return x - difference


A = np.array([[52, 30, 49, 28], [30, 50, 8, 44], [49, 8, 46, 16], [28, 44, 16, 22]], dtype=np.float64)
eigenVal, eigenVect = findEigen(A)

# print(np.array([eigenVect[:, 0]]).T.shape)
# print(F0(A, np.array([eigenVect[:, 0]]).T, eigenVal[0]))

newtonMethods(np.array([eigenVect[:, 0]]).T)

# print(f0v(eigenVal[0], A))
# print(f1v(np.array([eigenVect[:, 0]]).T))
