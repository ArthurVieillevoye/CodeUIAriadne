from pyariadne import *

def writeOnFile(lst):
    l = []
    # for el in lst:
    #     l.append((el[0], el[1]))
    with open('daemons.txt', 'w') as fp:
        fp.write('\n'.join('{},{}'.format(x[0], x[1]) for x in lst))

lst = []
lst.append((FloatDPApproximationMatrix([[1,2],[3,4]], dp), 'M1'))
lst.append((FloatDPApproximationMatrix([[5,6],[7,8]], dp), 'M2'))

writeOnFile(lst)