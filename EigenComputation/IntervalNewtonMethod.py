from pyariadne import *
from EigenComputation import Householder

def f(A, v, lamb):
    c = A * v - lamb * v
    pr = precision(128)
    f = join(c, 1 - (transpose(v) * v)/FloatMPValue(2, pr))
    return f


def df(A, v, lamb):
    n = len(v)
    pr = precision(128)
    I = FloatMPBoundsMatrix.identity(n, pr)
    # print(type(A - (lamb * I)))
    # print(type(FloatDPBounds((-1), dp)*v))
    topRow = cojoin(A - (lamb * I), -v)

    # print(topRow)
    bottomRow = cojoin(transpose(-v), FloatMPBounds(0, pr))
    # bottomRow = transpose(bottomRow)

    # print(type(topRow), '##### ', type(bottomRow))
    F = join(topRow, bottomRow)
    return F

def getIFirstElementsInVector(v, i):
    smallerV = []
    for j in range(i):
        smallerV.append(v[j])

    pr = precision(128)
    smallerV= FloatMPBoundsVector(smallerV, pr)
    return smallerV


def maxLenghtBounds(v):
    # pr = precision(128)
    maxRange = FloatMPApproximation(v[0].upper()) - FloatMPApproximation(v[0].lower())
    for i in range (1, len(v)):
        # print(v[0].upper() - v[0].lower())
        if cast_exact(v[0].upper() - v[0].lower()) > cast_exact(maxRange):
            maxRange = FloatMPApproximation(v[i].upper()) - FloatMPApproximation(v[i].lower())

    # print(type(maxRange))

    return maxRange

def intervalNewtonMethods(v,lamb, A):
    pr = precision(128)
    eps = FloatMPValue(Dyadic(1, 24), pr)

    v = cast_exact(v) + FloatMPBoundsVector(len(v), FloatMPBounds(-eps, +eps, pr))
    lamb = cast_exact(lamb) + FloatMPBounds(-eps, +eps, pr)
    A = cast_exact(A) + FloatMPBoundsMatrix(A.column_size(), A.row_size(), FloatMPBounds(-eps, +eps, pr))

    pr = precision(128)
    tolerance = cast_exact(FloatMPValue(Dyadic(1, 23), pr))

    counter = 0
    while cast_exact(maxLenghtBounds(v)) > tolerance and counter < 20:
        dfx = df(A, v, lamb)
        fx = f(FloatMPApproximationMatrix(cast_exact(A)), FloatMPApproximationVector(cast_exact(v)), FloatMPApproximation(cast_exact(lamb)))
        fx = cast_exact(fx) + FloatMPBoundsVector(len(fx), FloatMPBounds("-0", "+0", pr))

        deltax = solve(dfx, fx)

        lambBound = deltax[len(deltax) - 1]
        vBound = getIFirstElementsInVector(deltax, len(deltax) - 1)

        newV = cast_exact(v) - vBound
        newLamb = cast_exact(lamb) - lambBound

        if inconsistent(newV, v):
            print("There is no solutions")
            return 0,0
        elif refines(v, newV):
            print("problem.")
            return 1,0
        elif refines(newV, v):
            print("There is only one solution")
            newV = refinement(newV, v)
            newLamb = refinement(newLamb, lamb)
        else:
            print("There a solution")
            newV = refinement(newV, v)
            newLamb = refinement(newLamb, lamb)

        v = newV
        lamb = newLamb

        counter+=1

    return v, lamb

# if __name__ == '__main__':
    # pr = precision(128)
    # A = FloatMPApproximationMatrix([[2,6,4],[4,-1,0],[4,0,-3]], pr)
    # A = FloatMPApproximationMatrix([[52, 30, 49, 28], [30, 50, 8, 44], [49, 8, 46, 16], [28, 44, 16, 22]], pr)
    # A = FloatMPBoundsMatrix([[10, -1, 1], [-1, 30, 2], [1, 2, 20]], pr)
    # A = FloatMPBoundsMatrix([[1,7,3], [7,4,5], [3,5,0]], pr)
    # A = FloatMPBoundsMatrix([[2, -1, 1], [-1, 3, 2], [1, 2, 3]], pr)
    # A = FloatMPApproximationMatrix([[12,-51,4], [6,167,-68], [-4,24,-41]], pr)
    #A = FloatMPBoundsMatrix([[3,0,0],[0,2,0],[0,0,1]], pr)
    # eigenval, eigenvect = Householder.findEigenAriadne(A)
    #
    # lamb = eigenval[0]
    # v = eigenvect[0]
    # print("\nv:", v, "\nlambda:", lamb, "\n")
    # print("\nAv:", A*v, "\nlambda v:", lamb*v, "\n")
    #
    # newv, l = intervalNewtonMethods(v, lamb, A)
    # print("type", type(A))
    # print("\nAv:", A * newv - lamb * newv, "\n")
