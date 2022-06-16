import numpy as np
import math
from pyariadne import *


# def inverse_power_ariadne(A, lamb, v):
#     # tolerance = FloatMPApproximation("0.000001", A[0,0].precision())
#     # print(getMaxValueOfVector(A*v-lamb*v))
#     # while cast_exact(getMaxValueOfVector(A*v-lamb*v)) > cast_exact(tolerance):
#     for i in range(5):
#         I = FloatMPApproximationMatrix.identity(A.column_size(), A[0,0].precision())
#         y = solve((A-lamb*I), v)
#         print(getMaxValueOfVector(A * v - lamb * v))
#         nv = y/norm(y)
#         lamb = lamb + (dot(v,v)/dot(v,y))
#         print(A * nv - lamb * nv)
#     return lamb, nv

def inverse_power_ariadne(A, lamb, v):
    tolerance = FloatMPApproximation("0.000001", A[0,0].precision())
    # print(getMaxValueOfVector(A*v-lamb*v))
    nv = v
    counter = 0
    while cast_exact(getMaxValueOfVector(A*nv-lamb*nv)) > cast_exact(tolerance) and counter < 10:
        I = FloatMPApproximationMatrix.identity(A.column_size(), A[0,0].precision())
        y = solve((A-lamb*I), nv)
        nv = y/norm(y)
        lamb = lamb + (dot(nv,nv)/dot(nv,y))
        counter +=1
    return lamb, nv

def getMaxValueOfVector(v):
    max = FloatMPApproximation("0", v[0].precision())
    for i in range(len(v)):
        if cast_exact(max) < abs(cast_exact(v[i])):
            max = abs(v[i])
    return max

def euclNormAriadne(A):
    pr = precision(128)
    b = FloatMPApproximation(0, pr)
    for i in range(len(A)):
        b = b + (A[i] * A[i])
    return sqrt(b)

def getColumn(column_index, A):
    col = []
    for i in range(A.row_size()):
        col.append(A[i, column_index])

    pr = precision(128)
    return FloatMPApproximationVector(col, pr)

def copyAriadne(element):
    return eval(repr(element))

def placeAriadne(m, B):
    '''
    Place a smaller matrix B into a larger mXm identity matrix.
    The matrix B has to be placed into the bottom right of the identity matrix.
    This method is used in the QComputation methods in order to be able to multiply all the Q matrices.
    :param m: The size of the larger matrix. (m>size(B))
    :param B: The matrix we want to place in a larger matrix.
    :return: Te new matrix containing the B matrix.
    '''
    #TODO: Check that m>size(B)
    pr = precision(128)
    I = FloatMPApproximationMatrix.identity(m, pr)      #The identity matrix mXm
    o, p = B.row_size(), B.column_size()
    for i in range(m - o, m):
        for j in range(m - o, m):
            # Place the B matrix into the bottom right of the I matrix.
            I[i, j] = B[i - m + o, j - m + o]

    return I

def householderDecompositionAriadne(A):
    '''
    Compute the Q value for a matrix A
    The Q matrix is an orthogonal matrix (Q.T * Q = I)
    :param A: Input matrix (we want its Q matrix)
    :return: The Q matrix
    '''

    # Select a vector and
    a = []
    for i in range(A.row_size()):
        a.append(A[i, 0])

    pr = precision(128)
    a = FloatMPApproximationVector(a, pr)

    norm = euclNormAriadne(a)

    e = FloatMPApproximationVector.unit(len(a),0, pr)
    # This u vector will be used to compute the v vector.
    u = a - (norm * e)

    # Calculate the v value (V = u/||u||)
    # print(type((1 / euclNormAriadne(u)) * u))
    v = (1 / euclNormAriadne(u)) * u

    # Q calcuation
    tmp1 = []
    for i in range(len(v)):
        tmp2 = []
        for j in range(len(v)):
            tmp2.append(v[i] * v[j])
        tmp1.append(tmp2)

    I = FloatMPApproximationMatrix.identity(A.column_size(), pr)
    vMatrix = FloatMPApproximationMatrix(tmp1, pr)
    Q = I - (FloatMPApproximation(2, pr) * vMatrix)
    return Q

def getMaxValueBottomTriangularMatrix(A):
    max = FloatMPApproximation(0, precision(128))
    for i in range(A.row_size()):
        for j in range(i):
            if cast_exact(max) < abs(cast_exact(A[i,j])):
                max = abs(A[i,j])

    return max

def DecompositionQRAriadne(A):
    '''
    Estimated complexity n×n is : (3/4)*n^3
    Compute the Q and R values of the matrix A, such that A = Q*R.
    :param A: Matrix that we want to decompose in Q,R
    :return: the  and R matrices that comes from the A decomposition.
    '''
    # Complexity n×n est en : (3/4)*n^3
    n = A.column_size()

    B = copyAriadne(A)

    P = FloatMPApproximationMatrix.identity(n, precision(128))
    tolerance = FloatMPApproximation(0.0000000001, precision(128))
    counter = 0
    while cast_exact(getMaxValueBottomTriangularMatrix(B)) > cast_exact(tolerance) and counter < 300:
        (q, r) = gram_schmidt_orthogonalisation(B)
        P = P * q
        B = r * q  # Recompute the newA.

        counter +=1
    return P, B, counter


def getDiagonalElementAriadne(matrix):
    diag = []
    for i in range(matrix.row_size()):
        diag.append(matrix[i,i])
    pr = precision(128)
    return FloatMPApproximationVector(diag, pr)

def findEigenAriadne(A, precision):
    '''
    Find the eigenvalues and the eigenvector for the matrix A.
    Uses the QR decomposition in order to find them.
    :param A: The matrix we are interested in.
    :return: The eigenvectors and eigenvalues of A
    '''
    eigenValList = []
    eigenVectList = []

    APrime = copyAriadne(A)

    P, B, counter = DecompositionQRAriadne(APrime, precision)
    eigenVal = getDiagonalElementAriadne(B)

    eigenValList.append(eigenVal[0])
    eigenVectList.append(getColumn(0,P))

    for i in range(1, A.row_size()):
        l, v = inverse_power_ariadne(A, eigenVal[i], getColumn(i, P))
        eigenValList.append(l)
        eigenVectList.append(v)

    return eigenValList, eigenVectList, counter


# A = np.array([[52, 30, 49, 28], [30, 50, 8, 44], [49, 8, 46, 16], [28, 44, 16, 22]])
# A = np.array([[12,-51,4], [6,167,-68], [-4,24,-41]])
# A = np.array([[60, 91, 26], [60, 3, 75], [45, 90, 31]])
# A = np.array([[12,-51,14,11], [16,167,-68,11], [-14,24,-41,11], [-4,24,-41,11]])

# eigenVal, eigenVect = findEigen(A)
# print(eigenVal)
# print(eigenVect)

# print(A)
# print(findEigen(A))
#
# A = FloatDPApproximationMatrix([[52, 30, 49, 28], [30, 50, 8, 44], [49, 8, 46, 16], [28, 44, 16, 22]], dp)
# # print(A)
# pr = precision(128)
# A = FloatMPApproximationMatrix([[2,6,4],[4,-1,0],[4,0,-3]], pr)
# A = FloatMPApproximationMatrix([[12,-51,14,11], [16,167,-68,11], [-14,24,-41,11], [-4,24,-41,11]], precision(128))
# A = FloatMPApproximationMatrix([[12,-51,4, 32], [6,167,-68, 28], [-4,24,-41, 63]], pr)
# A = FloatMPApproximationMatrix([[12,-51,14,11], [16,167,-68,11], [-14,24,-41,11], [-4,24,-41,11]], precision(128))
# A = FloatMPApproximationMatrix([[3,1],[1,3]], pr)

# eigenval, eigenvect = findEigenAriadne(A)

# A = FloatMPApproximationMatrix([[1,2,3],[4,5,6],[7,8,9]], pr)
# print("$$$$$$$$$$$$$$$$$$$")
# A = FloatMPApproximationMatrix([[52, 30, 49, 28], [30, 50, 8, 44], [49, 8, 46, 16], [28, 44, 16, 22]], pr)
# # print(eigenval)
# # print(eigenvect)
#
# # print("$$$$$$$$$$$$$$$$$$$")
# print(getColumn(0, eigenvect))
# print(eigenval[0]*getColumn(0, eigenvect))
# print(A*getColumn(0, eigenvect))

# val, vect, tmp = findEigenAriadne(A, 0.000001)
# # print(val[0])
# print(A*vect[0]-val[0]*vect[0])
# print(tmp)
# print("Q*R-A", (Q*R)-A)
# print("Q", Q)
# print("R", R)

# print(eigenVal[0])
# print(np.array([eigenVect[:,0]]).T)
#
# eigenVal_eigenVect_verification(eigenVal[0],np.array([eigenVect[:,0]]).T, A)

# B = np.array([1,1,1])
# print(normQR(B))
# A = FloatDPApproximationVector([1,1,1], dp)
# print(norm(A))