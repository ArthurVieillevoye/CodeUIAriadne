import numpy as np
import math
from pyariadne import *


def normQR(x):
    '''
    Compute the norm of the vector X
    :param x: Vector for which we want the norm
    :return: the euclidian norm of the vector
    '''
    x = np.power(x, 2)
    norm = math.sqrt(sum(x))
    return norm


def householderDecomposition(A):
    '''
    Compute the Q value for a matrix A
    The Q matrix is an orthogonal matrix (Q.T * Q = I)
    :param A: Input matrix (we want its Q matrix)
    :return: The Q matrix
    '''

    # Select a vector and
    a = A[:, 0]
    norm = normQR(a)
    e = np.identity(len(a))
    e = e[:, 0]
    # This u vector will be used to compute the v vector.
    u = a - (norm * e)

    # Calculate the v value (V = u/||u||)
    v = np.array([(1 / normQR(u)) * u])

    # Q calcuation
    I = np.identity(v.shape[1])
    Q = I - (2 * (np.dot(v.T, v)))
    return Q


def place(m, B):
    '''
    Place a smaller matrix B into a larger mXm identity matrix.
    The matrix B has to be placed into the bottom right of the identity matrix.
    This method is used in the QComputation methods in order to be able to multiply all the Q matrices.
    :param m: The size of the larger matrix. (m>size(B))
    :param B: The matrix we want to place in a larger matrix.
    :return: Te new matrix containing the B matrix.
    '''
    #TODO: Check that m>size(B)
    I = np.identity(m)      #The identity matrix mXm
    o, p = B.shape
    for i in range(m - o, m):
        for j in range(m - o, m):
            # Place the B matrix into the bottom right of the I matrix.
            I[i, j] = B[i - m + o, j - m + o]

    return I


def QComputation(A):
    # https://ristohinno.medium.com/qr-decomposition-903e8c61eaab ?
    '''
    Estimated complexity n×n is : (3/4)*n^3
    Compute the Q and R values of the matrix A, such that A = Q*R.
    :param A: Matrix that we want to decompose in Q,R
    :return: the  and R matrices that comes from the A decomposition.
    '''
    # Complexity n×n est en : (3/4)*n^3
    m, n = A.shape      # Size of the A matrix
    Q = []              # List of all the Q values of the decomposition of the A matrix
    newA = A.copy()

    for i in range(m - 1):
        # Compute the Q value for the matrix newA
        q = householderDecomposition(newA)
        newA = np.round(np.dot(q, newA), 10)    # Recompute the newA.

        q = place(m, q)
        Q.append(q)
        # Update the newA. Since q*A gives a column of zero under the diagonal, I deleted the column and the row in
        # order to continue finding.
        newA = np.delete(newA, (0), axis=0)
        newA = np.delete(newA, (0), axis=1)

    # Compute the total Q matrix for the A matrix
    QTot = np.dot(Q[0], Q[1])
    for i in range(2, len(Q)):
        QTot = np.dot(QTot, Q[i])

    # Compute the R matrix
    R = np.dot(QTot.T, A)
    R = np.round(R, 10)
    return QTot, R


def findEigen(A):
    '''
    Find the eigenvalues and the eigenvector for the matrix A.
    Uses the QR decomposition in order to find them.
    :param A: The matrix we are interested in.
    :return: The eigenvectors and eigenvalues of A
    '''
    X = A.copy()
    pQ = np.identity(A.shape[0])

    # Iterate to converge to the correct eigenvalues and eigenvectors.
    for i in range(100):
        Q, R = QComputation(X)
        pQ = np.dot(pQ, Q)
        X = np.dot(R, Q)
        #TODO: instead of 100, check for A-diag(A) approx 0: Put tolerance as input
        #TODO: Use Ariadne's  Matrix[FloatXPApproximation]


    eigenVal = X.diagonal()
    # TODO: Keep the closest one to a given estimation.
    return eigenVal, pQ


def eigenVal_eigenVect_verification(l, v, A):
    I = np.identity(A.shape[0])
    print(np.dot(A-(l*I),v))
    print(np.isclose(np.dot(A-(l*I),v), 0))
    # print(np.isclose(np.dot(A-(l*I),v)))


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################


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

def shrinkMatrixAriadne(matrix):
    m, n = matrix.column_size(), matrix.row_size()
    pr = precision(128)
    answer = FloatMPApproximationMatrix.identity(m-1, pr)
    for i in range(1, n):
        for j in range(1, m):
            answer[i-1,j-1] = matrix[i,j]

    return answer

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


def DecompositionQRAriadne(A):
    '''
    Estimated complexity n×n is : (3/4)*n^3
    Compute the Q and R values of the matrix A, such that A = Q*R.
    :param A: Matrix that we want to decompose in Q,R
    :return: the  and R matrices that comes from the A decomposition.
    '''
    # Complexity n×n est en : (3/4)*n^3
    n = A.column_size()      # Size of the A matrix
    Q = []              # List of all the Q values of the decomposition of the A matrix

    newA = copyAriadne(A)
    for i in range(n - 1):
        # Compute the Q value for the matrix newA
        q = householderDecompositionAriadne(newA)
        newA = q * newA   # Recompute the newA.

        q = placeAriadne(n, q)
        Q.append(q)
        # Update the newA. Since q*A gives a column of zero under the diagonal, I deleted the column and the row in
        # order to continue finding.
        newA = shrinkMatrixAriadne(newA)

    # Compute the total Q matrix for the A matrix

    QTot = Q[0] * Q[1]
    for i in range(2, len(Q)):
        QTot = QTot * Q[i]

    # print("hello", type(QTot))
    # Compute the R matrix
    R = transpose(QTot) * A
    # R = np.round(R, 10)
    return QTot, R

def getDiagonalElementAriadne(matrix):
    diag = []
    for i in range(matrix.row_size()):
        diag.append(matrix[i,i])
    pr = precision(128)
    return FloatMPApproximationVector(diag, pr)

def findEigenAriadne(A):
    '''
    Find the eigenvalues and the eigenvector for the matrix A.
    Uses the QR decomposition in order to find them.
    :param A: The matrix we are interested in.
    :return: The eigenvectors and eigenvalues of A
    '''
    X = copyAriadne(A)
    pr = precision(128)
    pQ = FloatMPApproximationMatrix.identity(A.row_size(), pr)

    # Iterate to converge to the correct eigenvalues and eigenvectors.
    for i in range(50):
        Q, R = DecompositionQRAriadne(X)
        pQ = pQ * Q
        X = R * Q


    eigenVal = getDiagonalElementAriadne(X)
    # TODO: Keep the closest one to a given estimation.
    return eigenVal, pQ


# A = np.array([[52, 30, 49, 28], [30, 50, 8, 44], [49, 8, 46, 16], [28, 44, 16, 22]])
# A = np.array([[12,-51,4], [6,167,-68], [-4,24,-41]])
# A = np.array([[60, 91, 26], [60, 3, 75], [45, 90, 31]])
# A = np.array([[12,-51,14,11], [16,167,-68,11], [-14,24,-41,11], [-4,24,-41,11]])

# eigenVal, eigenVect = findEigen(A)
# print(eigenVal)
# print(eigenVect)

# print(A)
# print(findEigen(A))
# A = FloatDPApproximationMatrix([[12,-51,4], [6,167,-68], [-4,24,-41]], dp)
# A = FloatDPApproximationMatrix([[52, 30, 49, 28], [30, 50, 8, 44], [49, 8, 46, 16], [28, 44, 16, 22]], dp)
# # print(A)
# eigenval, eigenvect = findEigenAriadne(A)
# print("$$$$$$$$$$$$$$$$$$$")
# # print(eigenval)
# # print(eigenvect)
#
# # print("$$$$$$$$$$$$$$$$$$$")
# print(getColumn(0, eigenvect))
# print(eigenval[0]*getColumn(0, eigenvect))
# print(A*getColumn(0, eigenvect))

# print(eigenVal[0])
# print(np.array([eigenVect[:,0]]).T)
#
# eigenVal_eigenVect_verification(eigenVal[0],np.array([eigenVect[:,0]]).T, A)

# B = np.array([1,1,1])
# print(normQR(B))
# A = FloatDPApproximationVector([1,1,1], dp)
# print(norm(A))