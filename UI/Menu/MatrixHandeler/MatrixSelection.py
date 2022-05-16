from tkinter import *
import numpy as np
import json


class Matrices:
    def __init__(self, root, textArea):
        self.matrices = self.readFromFile()
        self.root = root
        self.textArea = textArea

    def gtc(self, i):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.matrices[i][0])

    def addMatrix(self, matrix, name=''):
        self.matrices.append((matrix,name))
        self.writeOnFile(self.matrices)

    def getMatrices(self):
        return self.matrices

    def printMatrix(self, i):
        sentence = "Matrix : " + self.matrices[i][1] + " = " + str(self.matrices[i][0]) +'\n'
        self.textArea.printInOutputArea(sentence)

    def writeOnFile(self,lst):
        l = []
        for el in lst:
            l.append((el[0].tolist(), el[1]))
        with open('data.json', 'w') as f:
            json.dump(l, f)

    # read the file
    def readFromFile(self):
        list2 = []
        try:
            with open('data.json') as f:
                lst1 = [tuple(x) for x in json.load(f)]

                for el in lst1:
                    list2.append((np.array(el[0]), el[1]))
        except:
            pass
        return list2


    def seeMatrices(self):
        var = IntVar()
        window = Frame(self.root)
        for i in range(len(self.matrices)):
            text = self.matrices[i][1] + ': ' + str(np.shape(self.matrices[i][0]))
            Radiobutton(window, text=text, padx=20, variable=var, value=i).pack(anchor=W)
            #TODO: Add the name of the matrix.


        buttonSee = Button(window, text="See Matrix", width=10, padx=5, pady=5, command=lambda: self.printMatrix(var.get()))
        buttonSee.pack(anchor=W)
        buttonCopy = Button(window, text="CopyMatrix", width=10, padx=5, pady=5, command=lambda: self.gtc(var.get()))
        buttonCopy.pack(anchor=W)

        window.grid(row=0, column=1, sticky=N + S + E + W)
