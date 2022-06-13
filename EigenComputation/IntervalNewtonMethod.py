from pyariadne import *
from EigenComputation import Householder


def f(A, v, lamb):
    c = A * v - lamb * v
    # print(len(c))
    # print(transpose(c))
    # print(type(1 - (transpose(v) * v)))
    pr = precision(128)
    f = join(c, 1 - (transpose(v) * v)/FloatMPBounds(2, pr))
    return f


def df(A, v, lamb):
    n = len(v)
    pr = precision(128)
    I = FloatMPBoundsMatrix.identity(n, pr)
    # print(type(A - (lamb * I)))
    # print(type(FloatDPBounds((-1), dp)*v))
    topRow = cojoin(A - (lamb * I), -v)

    print(topRow)

    bottomRow = cojoin(transpose(-v), FloatMPBounds(0, pr))
    # bottomRow = transpose(bottomRow)

    print(type(topRow), '##### ', type(bottomRow))
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
        print(v[0].upper() - v[0].lower())
        if cast_exact(v[0].upper() - v[0].lower()) > cast_exact(maxRange):
            maxRange = FloatMPApproximation(v[i].upper()) - FloatMPApproximation(v[i].lower())

    return maxRange

def intervalNewtonMethods(v,lamb, A):
    print("v", v)
    print("A*v", A * cast_exact(v))
    print("lamb*v", lamb * v)

    pr = precision(128)
    eps = FloatMPValue(Dyadic(1, 10), pr)
    v = cast_exact(v) + FloatMPBoundsVector(len(v), FloatMPBounds(-eps, +eps, pr))
    lamb = cast_exact(lamb) + FloatMPBounds(-eps, +eps, pr)
    A = cast_exact(A) + FloatMPBoundsMatrix(A.column_size(), A.row_size(), FloatMPBounds(-eps, +eps, pr))

    print("types", type(v), type(lamb), type(A))
    # print("A*v", A * cast_exact(v))
    # print("lamb*v", cast_exact(lamb) * cast_exact(v))


    print("v:", v)
    print("inv(A)", inverse(A))
    assert (type(lamb) == FloatDPBounds or type(lamb) == FloatMPBounds)

    # precision = cast_exact(FloatDPApproximation("0.00000000000000001", dp))

    for i in range(5):

        dfx = df(A, v, lamb)
        fx = f(A, FloatMPBoundsVector(cast_exact(v)), FloatMPBounds(cast_exact(lamb)))
        fx = fx + FloatMPBoundsVector(len(fx), FloatMPBounds(-0, +0, pr))
        # print(df.column_size(), ' ++++++', df.row_size())
        print(len(fx))

        print("dfx:", dfx, type(dfx))
        print("fx:", fx, type(fx))

        print("inv(dfx):", inverse(dfx))
        deltax = solve(dfx, fx)
        print(type(deltax))
        print("deltax:", deltax, type(deltax))

        # print((cast_exact(v)))
        # print(lamb)

        lambBound = deltax[len(deltax) - 1]
        vBound = getIFirstElementsInVector(deltax, len(deltax) - 1)
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

        v = newV
        lamb = newLamb

    print("A*v", A * cast_exact(newV))
    print("lamb*v", cast_exact(newLamb) * cast_exact(newV))

    return v, lamb

if __name__ == '__main__':
    pr = precision(128)
    A = FloatMPBoundsMatrix([[2,-1,1],[-1,3,2],[1,2,3]], pr)
    # A = FloatDPApproximationMatrix([[12,-51,4], [6,167,-68], [-4,24,-41]], dp)
    eigenval, eigenvect = Householder.findEigenAriadne(A)

    v = Householder.getColumn(0, eigenvect)
    lamb = eigenval[0]

    intervalNewtonMethods(v, lamb, A)