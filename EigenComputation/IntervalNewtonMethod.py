from pyariadne import *


# print(dir())

######################

def f(A, v, lamb):
    f = join(A * v - lamb * v, 1 - transpose(v) * v)
    return f


def df(A, v, lamb):
    n = len(v)
    print(n, A.row_size())
    I = FloatDPBoundsMatrix.identity(n, dp)
    topRow = join(A - (lamb * I), lamb * transpose(v))
    bottomRow = join(transpose(v), 0)

    F = join(topRow, bottomRow)
    return F


def intervalNewtonMethod(A, vect, lamb):
    assert (type(lamb) == FloatDPBounds or type(lamb) == FloatMPBounds)
    e = 1
    # e = FloatDPBoundsVector([FloatDPBounds(3, 1, dp), FloatDPBounds(3, 1, dp)])

    v1 = vect + e
    v2 = (vect + e) / FloatDPBounds(2, dp)

    v = join(v1, v2)

    v = cast_exact(v) - solve(df(A, v, lamb), f(A, v, lamb))


if __name__ == '__main__':
    A = FloatDPBoundsMatrix([[1,2],[3,4]], dp)
    v = FloatDPBoundsVector([2, 3], dp)
    lamb = FloatDPBounds(9, dp)

    assert (type(lamb) == FloatDPBounds or type(lamb) == FloatMPBounds)
    # e = 1
    e = FloatDPBoundsVector([1, 1], dp)

    v1 = v - e
    v2 = (v + e)

    v = join(v1, v2)
    print(len(v))

    v = cast_exact(v) - solve(df(A, v, lamb), f(A, v, lamb))
    #
    # print(refines(v1, v2))
    #
    # if refines(v1, v2):
    #     print('we got a problem')

    print(cast_exact(e))
# else:
#	print('All right')
