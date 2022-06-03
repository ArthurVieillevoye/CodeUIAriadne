from pyariadne import *


# print(dir())

######################

def f(A, v, lamb):
    c = A * v - lamb * v
    # print(len(c))
    # print(transpose(c))
    # print(type(1 - (transpose(v) * v)))
    f = join(c, 1 - (transpose(v) * v)/FloatDPApproximation(2, dp)) # TODO: need to divide by 2 the vT*v
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
        if FloatDPApproximation(v[i].upper()) - FloatDPApproximation(v[i].lower()) > maxRange:
            maxRange = FloatDPApproximation(v[i].upper()) - FloatDPApproximation(v[i].lower())

    return maxRange


# def intervalNewtonMethod(A, vect, lamb):
#     assert (type(lamb) == FloatDPBounds or type(lamb) == FloatMPBounds)
#     e = 1
#     # e = FloatDPBoundsVector([FloatDPBounds(3, 1, dp), FloatDPBounds(3, 1, dp)])
#
#     v1 = vect + e
#     v2 = (vect + e) / FloatDPBounds(2, dp)
#
#     v = join(v1, v2)
#
#     v = cast_exact(v) - solve(df(A, v, lamb), f(A, v, lamb))


if __name__ == '__main__':
    #A = FloatDPBoundsMatrix([[2,-1,1],[-1,3,2],[1,2,3]], dp)
    A = FloatDPBoundsMatrix([[3,-1,1],[-1,4,2],[1,2,5]], dp)
    eps = 0.001
    eps=0
    # v = FloatDPBoundsVector([{x_(1 - eps): x_(1 + eps)}, {x_(-1): x_(-1 + eps)}, {x_(-1): x_(-1 + eps)}], dp)
    v = FloatDPBoundsVector([{63:64},{59:60},{-50:-49}],dp)/FloatDPBounds(100,dp)

    # lamb = FloatDPBounds(Decimal(1.2),Decimal(1.3),dp)
    lamb = FloatDPBounds(10, 11, dp) / 10

    print("v:",v)
    print("inv(A)",inverse(A))
    assert (type(lamb) == FloatDPBounds or type(lamb) == FloatMPBounds)
    # e = 1
    # e = FloatDPBoundsVector([1, 1], dp)
    #
    # v1 = v - e
    # v2 = (v + e)


    # I=FloatDPBoundsMatrix.identity(3,dp)
    # z=FloatDPBounds(0,dp)
    # J=join(cojoin(A-lamb*I,v),cojoin(transpose(v),z))
    # print("J:", J)
    # print("inv(J)",inverse(J))
    # v = join(v1, v2)
    # print(len(v))
    # print(v)
    precision = 0.0001
    while maxLenghtBounds(v) > precision:
        # TODO: find the boolean value.

        dfx = df(A, v, lamb)
        fx = f(A, FloatDPBoundsVector(cast_exact(v)), FloatDPBounds(cast_exact(lamb)))
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

        print("oldV: ", v)
        print("newV: ", newV)
        if inconsistent(newV, v):
            print("There is no solutions")
        elif refines(newV, v):
            print("There is only one solution")
            newV = refinement(newV, v)
        else:
            newV = refinement(newV, v)

        break

    print("newV:", newV)

