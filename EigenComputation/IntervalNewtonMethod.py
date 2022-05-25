from pyariadne import *


# print(dir())

######################

def f(A, v, lamb):
    c = A * v - lamb * v
    # print(len(c))
    # print(transpose(c))
    # print(type(1 - (transpose(v) * v)))
    f = join(c, 1 - (transpose(v) * v))
    return f


def df(A, v, lamb):
    n = len(v)
    I = FloatDPBoundsMatrix.identity(n, dp)
    # print(type(A - (lamb * I)))
    # print(type(FloatDPBounds((-1), dp)*v))
    topRow = cojoin(A - (lamb * I), FloatDPBounds((-1), dp)*v)

    print(topRow)

    bottomRow = cojoin(FloatDPBounds((-1), dp)*transpose(v), FloatDPBounds(0, dp))
    # bottomRow = transpose(bottomRow)

    print(type(topRow), '##### ', type(bottomRow))
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
    eps = 0.5
    v = FloatDPBoundsVector([{x_(2-eps):x_(2+eps)},{x_(3):x_(3+eps)}], dp)
    lamb = FloatDPBounds(9, dp)

    assert (type(lamb) == FloatDPBounds or type(lamb) == FloatMPBounds)
    # e = 1
    e = FloatDPBoundsVector([1, 1], dp)

    v1 = v - e
    v2 = (v + e)

    # v = join(v1, v2)
    # print(len(v))
    # print(v)

    df = df(A, v, lamb)
    f = f(A, v, lamb)
    print(df.column_size(), ' ++++++', df.row_size())
    print(len(f))

    tmp = solve(df, f)

    v = cast_exact(v) - tmp
    #
    # print(refines(v1, v2))
    #
    # if refines(v1, v2):
    #     print('we got a problem')

    print(cast_exact(e))
# else:
#	print('All right')
