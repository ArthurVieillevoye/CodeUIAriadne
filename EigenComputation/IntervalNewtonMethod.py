from pyariadne import *
from Householder import *


def f(A, v, lamb):
    c = A * v - lamb * v
    # print(len(c))
    # print(transpose(c))
    # print(type(1 - (transpose(v) * v)))
    f = join(c, 1 - (transpose(v) * v)/FloatDPBounds(2, dp))
    return f


def df(A, v, lamb):
    n = len(v)
    I = FloatDPBoundsMatrix.identity(n, dp)
    # print(type(A - (lamb * I)))
    # print(type(FloatDPBounds((-1), dp)*v))
    topRow = cojoin(A - (lamb * I), -v)

    print(topRow)

    bottomRow = cojoin(transpose(-v), FloatDPBounds(0, dp))
    # bottomRow = transpose(bottomRow)

    print(type(topRow), '##### ', type(bottomRow))
    F = join(topRow, bottomRow)
    return F

def getIFirstElementsInVector(v, i):
    smallerV = []
    for j in range(i):
        smallerV.append(v[j])
    smallerV= FloatDPBoundsVector(smallerV, dp)
    return smallerV


def maxLenghtBounds(v):
    maxRange = FloatDPApproximation(v[0].upper()) - FloatDPApproximation(v[0].lower())
    for i in range (1, len(v)):
        print(v[0].upper() - v[0].lower())
        if cast_exact(v[0].upper() - v[0].lower()) > cast_exact(maxRange):
            maxRange = FloatDPApproximation(v[i].upper()) - FloatDPApproximation(v[i].lower())

    return maxRange

if __name__ == '__main__':
    #A = FloatDPBoundsMatrix([[2,-1,1],[-1,3,2],[1,2,3]], dp)
    A = FloatDPApproximationMatrix([[12,-51,4], [6,167,-68], [-4,24,-41]], dp)
    eigenval, eigenvect = findEigenAriadne(A)

    v = getColumn(0, eigenvect)
    lamb = eigenval[0]

    eps = FloatDPValue(Dyadic(1,20), dp)
    v = cast_exact(v) + FloatDPBoundsVector(len(v), FloatDPBounds(-eps, +eps, dp))
    lamb = cast_exact(lamb) + FloatDPBounds(-eps, +eps, dp)
    A = cast_exact(A) + FloatDPBoundsMatrix(A.column_size(), A.row_size(), FloatDPBounds(-eps, +eps, dp))

    print("types", type(v), type(lamb), type(A))


    print("v:",v)
    print("inv(A)",inverse(A))
    assert (type(lamb) == FloatDPBounds or type(lamb) == FloatMPBounds)

    precision = cast_exact(FloatDPApproximation("0.00000000000000001", dp))

    while cast_exact(maxLenghtBounds(v)) > precision:

        dfx = df(A, v, lamb)
        fx = f(A, FloatDPBoundsVector(cast_exact(v)), FloatDPBounds(cast_exact(lamb)))
        # fx = fx + FloatDPBoundsVector(len(fx), FloatDPBounds(-0, +0, dp))
        # print(df.column_size(), ' ++++++', df.row_size())
        print(len(fx))

        print("dfx:", dfx, type(dfx))
        print("fx:", fx, type(fx))

        print("inv(dfx):",inverse(dfx))
        deltax = solve(dfx, fx)
        print(type(deltax))
        print("deltax:",deltax,type(deltax))

        print((cast_exact(v)))
        print(lamb)

        lambBound = deltax[len(deltax)-1]
        vBound = getIFirstElementsInVector(deltax, len(deltax)-1)
        print("vBounds", vBound)
        newV = cast_exact(v) - vBound
        newLamb = cast_exact(lamb) - lambBound

        print("oldV: ", v)
        print("newV: ", newV)
        if inconsistent(newV, v):
            print("There is no solutions")
        elif refines(newV, v):
            print("There is only one solution")
            newV = refinement(newV, v)
            newLamb = refinement(newLamb, lamb)
        else:
            newV = refinement(newV, v)
            newLamb = refinement(newLamb, lamb)

        print("A*v", A*cast_exact(newV))
        print("lamb*v", cast_exact(newLamb)*cast_exact(newV))
        break