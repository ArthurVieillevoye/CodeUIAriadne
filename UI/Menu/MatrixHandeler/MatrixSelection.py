from tkinter import *
import numpy as np
import json
from pyariadne import *


class Matrices:
    def __init__(self, root, textArea):
        self.matrices = self.readDatabaseFromFile()
        self.root = root
        self.frame = Frame(self.root)
        self.textArea = textArea
        self.histrow = 0
        self.histcol = 0

    def gtc(self, i):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.matrices[i][0])

    def addMatrix(self, matrix, name=''):
        if name != '':
            self.matrices.append((matrix, name))
            self.writeOnFile(self.matrices)
        else:
            self.textArea.printInOutputArea('Error: Your matrix must have a name')

    def getMatrices(self):
        return self.matrices

    def printMatrix(self, i):
        sentence = "Matrix : " + self.matrices[i][1] + " = " + repr(self.matrices[i][0]) + '\n'
        self.textArea.printInOutputArea(sentence)

    def writeOnFile(self, lst):
        with open('MatrixDatabase.txt', 'w') as fp:
            fp.write('\n'.join('{};{}'.format(repr(x[0]), x[1]) for x in lst))

    # read the file
    def readDatabaseFromFile(self):
        mylist = []
        try:
            with open('MatrixDatabase.txt') as f:
                for i in f:
                    a, b = i.split(';')
                    mylist.append((FloatDPApproximationMatrix(eval(a), dp), b))
            print(type(mylist[0][0]))
        except:
            pass
        return mylist

    def showSelectedMatrix(self, i):
        window = Frame(self.frame)

        matrix = self.matrices[i][0]
        m, n = 0, 1
        # m,n = np.shape(matrix)
        if self.histrow != int(m) or self.histcol != int(n):
            self.histrow = int(m)
            self.histcol = int(n)
            self.row = int(m)
            self.col = int(n)

        # Delete all the elements previously present on the grid.
        # for label in self.root.grid_slaves():
        #     if int(label.grid_info()["column"]) > 3:
        #         label.destroy()

        # Show the column numbers
        for c in range(self.col):
            l = Label(window, text=str(c))
            l.grid(row=0, column=c + 1)

        # Show the row numbers
        self.entries = []
        for r in range(self.row):
            entries_row = []
            l = Label(window, text=str(r))
            l.grid(row=r, column=0)
            # Add the entries that will contains the values.
            for c in range(self.col):
                singleEntry = Entry(window, width=5)  # 5 chars
                try:
                    singleEntry.insert('end', matrix[r, c])
                except:
                    singleEntry.insert('end', 0)
                singleEntry.grid(row=r, column=c + 1)
                entries_row.append(singleEntry)
            self.entries.append(entries_row)

        saveButton = Button(window, text='save changes', padx=5, pady=5, command=lambda: self.get_data(i))
        saveButton.grid(row=self.row + 1, column=1, sticky="ew")
        window.grid(row=0, column=1, sticky=N + S + E + W)

        # addRowButton = Button(self.root, text='+', command=self.addRow)
        # addRowButton.grid(row=self.row, column=5)
        # addColButton = Button(self.root, text='+', command=self.addCol)
        # addColButton.grid(row=0, column=self.col + 6)

    def get_data(self, i, ret=False):
        """
        Get the elements entered into the grid created in the addMatrixWindow.
        Create a matrix from those elements.
        """
        selectedMatrix = self.matrices.pop(i)

        demand = np.zeros((self.row, self.col))
        for r, row in enumerate(self.entries):
            for c, entry in enumerate(row):
                text = entry.get()
                demand[r, c] = float(text)

        if ret:
            return demand
        else:
            self.addMatrix(demand, self.matrices[i][1])

    def deleteMatrix(self, i):
        self.matrices.pop(i)
        self.writeOnFile(self.matrices)
        for el in self.frame.grid_slaves():
            el.grid_forget()

        self.seeMatrices()

    def seeMatrices(self):
        var = IntVar()
        window = Frame(self.frame)
        for i in range(len(self.matrices)):
            text = self.matrices[i][1] + ': ' + str(np.shape(self.matrices[i][0]))
            Radiobutton(window, text=text, padx=20, variable=var, value=i).pack(anchor=W)
            # TODO: Add the name of the matrix.

        buttonSee = Button(window, text="See Matrix", width=10, padx=5, pady=5,
                           command=lambda: self.showSelectedMatrix(var.get()))
        buttonSee.pack(anchor=W)
        buttonSee = Button(window, text="Print Matrix", width=10, padx=5, pady=5,
                           command=lambda: self.printMatrix(var.get()))
        buttonSee.pack(anchor=W)
        buttonCopy = Button(window, text="Copy Matrix", width=10, padx=5, pady=5, command=lambda: self.gtc(var.get()))
        buttonCopy.pack(anchor=W)
        buttonCopy = Button(window, text="Delete Matrix", width=10, padx=5, pady=5,
                            command=lambda: self.deleteMatrix(var.get()))
        buttonCopy.pack(anchor=W)

        window.grid(row=0, column=0, sticky=N + S + E + W)
        self.frame.grid(row=0, column=1, sticky=N + S + E + W)
