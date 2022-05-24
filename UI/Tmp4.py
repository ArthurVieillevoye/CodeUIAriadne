import numpy as np

hello = '[[1,2,3 ; 4,5,6]]'

lst = []
hello = hello.replace("[", "")
hello = hello.replace("]", "")
hello = hello.replace(" ", "")
print(hello)

hello1 = hello.split(';')
print(hello1)
for el in hello1:
    listtmp = '[' + el + ']'
    lst.append(eval(listtmp))

print(lst[0][0])