from tkinter import *
import numpy as np
import pandas as pd
from tkinter import filedialog


class MatrixCreationWindow:
    """
    This class contains all the information for the input of a matrix into the file.
    It contains 2 matrix creation element: One where you can write it yourself and another one where you can upload
    the matrix from a file.
    """

    def __init__(self, root, textArea, row=0, col=0, matrixMemory=None):
        self.entries = []
        self.row = row
        self.col = col
        self.root = root
        self.matrix = []
        self.histrow = 0
        self.histcol = 0
        self.matrixMemory = matrixMemory
        self.textArea = textArea
        self.entryRow = 0
        self.entryColumns = 0
        self.root.focus_set()

    def addMatrixWindow(self):
        """
        Create a new window for the user to enter the matrix of its choice.
        """

        for label in self.root.grid_slaves():
            if int(label.grid_info()["column"]) > 0:
                label.destroy()

        # self.buttonWrite.grid_remove()
        # self.buttonMatrixFromFile.grid_remove()

        # Creates the labels and the entry boxes for the row and column numbers.

        label1 = Label(self.root, text="row")
        label1.grid(row=0, column=1)
        self.e1 = Entry(self.root, width=10, borderwidth=5)
        self.e1.grid(row=0, column=2)

        label2 = Label(self.root, text="Column")
        label2.grid(row=1, column=1)
        self.e2 = Entry(self.root, width=10, borderwidth=5)
        self.e2.grid(row=1, column=2)

        label3 = Label(self.root, text="Name")
        label3.grid(row=2, column=1)
        self.e3 = Entry(self.root, width=10, borderwidth=5)
        self.e3.grid(row=2, column=2)

        # self.e1.bind_all('<Return>', lambda event: self.updateMatrixWindow)
        # self.e2.bind_all('<Return>', lambda event: self.updateMatrixWindow)

        buttonCreateMatrix = Button(self.root, text="Enter Size", padx=5, pady=5, command=self.getRowAndColumnSize)
        buttonCreateMatrix.grid(row=0, column=3, sticky="ew")

    def getRowAndColumnSize(self):
        # Enter the column numbers.
        try:
            if self.histrow != int(self.e1.get()) or self.histcol != int(self.e2.get()):
                self.histrow = int(self.e1.get())
                self.histcol = int(self.e2.get())
                self.row = int(self.e1.get())
                self.col = int(self.e2.get())
                self.updatMatrixWindow()
        except:
            self.textArea.printInOutputArea('You did not correctly entered the size of the matrix. Only integer allowed.')

    def updatMatrixWindow(self):

        # Delete all the elements previously present on the grid.
        for label in self.root.grid_slaves():
            if int(label.grid_info()["column"]) > 3:
                label.destroy()

        # Show the column numbers
        for c in range(self.col):
            l = Label(self.root, text=str(c))
            l.grid(row=0, column=c + 5)

        # Show the row numbers
        self.entries = []
        for r in range(self.row):
            entries_row = []
            l = Label(self.root, text=str(r))
            l.grid(row=r, column=4)
            # Add the entries for the values.
            for c in range(self.col):
                singleEntry = Entry(self.root, width=5, validatecommand=self.updateIndexes)  # 5 chars
                singleEntry.bind("<Left>", lambda e:self.left(e))
                singleEntry.bind("<Right>", lambda e:self.right(e))
                singleEntry.bind("<Up>", lambda e:self.up(e))
                singleEntry.bind("<Down>", lambda e:self.down(e))
                try:
                    singleEntry.insert('end', self.matrix[r, c])
                except:
                    singleEntry.insert('end', 0)
                singleEntry.grid(row=r, column=c + 5)
                entries_row.append(singleEntry)
            self.entries.append(entries_row)
        self.entries[self.entryRow][self.entryColumns].focus_set()

        saveButton = Button(self.root, text='Save matrix', padx=5, pady=5, command=self.get_data)
        saveButton.grid(row=2, column=3, sticky="ew")

        addRowButton = Button(self.root, text='+', command=self.addRow)
        addRowButton.grid(row=self.row, column=5)
        addColButton = Button(self.root, text='+', command=self.addCol)
        addColButton.grid(row=0, column=self.col + 6)

    def updateIndexes(self):
        print('hello')

    def left(self, event):
        try:
            self.entryColumns = self.entryColumns - 1
            self.entries[self.entryRow][self.entryColumns].focus()
        except:
            pass

    def right(self, event):
        try:
            self.entryColumns = self.entryColumns + 1
            print(type(self.entries[self.entryRow][self.entryColumns]))
            self.entries[self.entryRow][self.entryColumns].focus()
        except:
            pass

    def up(self, event):
        try:
            self.entryRow = self.entryRow - 1
            self.entries[self.entryRow][self.entryColumns].focus()
        except:
            pass

    def down(self, event):
        try:
            self.entryRow = self.entryRow + 1
            self.entries[self.entryRow][self.entryColumns].focus()
        except:
            pass

    def addRow(self):
        self.matrix = self.get_data(True)
        self.row = self.row + 1
        self.updateMatrixWindow()

    def addCol(self):
        self.matrix = self.get_data(True)
        self.col = self.col + 1
        self.updateMatrixWindow()

    def get_data(self, ret=False):
        """
        Get the elements entered into the grid created in the addMatrixWindow.
        Create a matrix from those elements.
        """
        demand = np.zeros((self.row, self.col))
        for r, row in enumerate(self.entries):
            for c, entry in enumerate(row):
                text = entry.get()
                demand[r, c] = float(text)

        if ret:
            return demand
        else:
            self.matrixMemory.addMatrix(demand, self.e3.get())

    def addMatrixTextWindow(self):
        for label in self.root.grid_slaves():
            if int(label.grid_info()["column"]) > 0:
                label.destroy()

        label1 = Label(self.root, text='Enter your matrix in python or matlab form')
        label1.grid(row=0, column=1, columnspan=2)

        label2 = Label(self.root, text='Matrix: ')
        label2.grid(row=1, column=1)
        matrixEntry = Entry(self.root, width=100)
        matrixEntry.grid(row=1, column=2)

        label = Label(self.root, text="Name of the matrix:")
        label.grid(row=2, column=1)
        entryName = Entry(self.root, width=50)
        entryName.grid(row=2, column=2, sticky=W)

        button = Button(self.root, text='save Matrix', padx=5, pady=5,
                        command=lambda: self.decodeEnteredMatrix(matrixEntry.get(), entryName.get()))
        button.grid(row=3, column=1)

    def decodeEnteredMatrix(self, matrix, name):
        passed = True
        try:
            self.matrixMemory.addMatrix(np.array(eval(matrix)), name)
        except:
            passed = False
        try:
            passed = True
            myMatrix = []
            matrix = matrix.replace("[", "")
            matrix = matrix.replace("]", "")
            matrix = matrix.replace(" ", "")

            matrix = matrix.split(';')
            for el in matrix:
                listTmp = '[' + el + ']'
                myMatrix.append(eval(listTmp))
            self.matrixMemory.addMatrix(np.array(myMatrix), name)
        except:
            passed = False

        if not passed:
            self.textArea.printInOutputArea('You did not enter the matrix in a correct form')

    def getMatrixFromFile(self):
        """
        This method is used if the user wants to open a .xcel file containing a matrix.
        Read this file and return the matrix contained into the .xcel file.s
        """
        for label in self.root.grid_slaves():
            if int(label.grid_info()["column"]) > 0:
                label.destroy()

        open_file_loc = filedialog.askopenfilename()
        if open_file_loc != '':
            try:
                df = pd.read_excel(open_file_loc, header=None)
                myMatrix = df.to_numpy()
                self.nameWindowForUploadedMatrices(myMatrix)
            except:
                try:
                    print('hello')
                    df = pd.read_csv(open_file_loc, header=None, sep=';')
                    print('df: ', df)
                    # df.values
                    myMatrix = df.to_numpy()
                    self.nameWindowForUploadedMatrices(myMatrix)
                except:
                    self.textArea.printInOutputArea("Error: File is not in the correct format (.csv or .xcel)")

    def nameWindowForUploadedMatrices(self, myMatrix):
        label = Label(self.root, text="Name of the matrix:")
        label.grid(row=0, column=1)
        e = Entry(self.root, width=30, borderwidth=5)
        e.grid(row=1, column=1)

        button = Button(self.root, text='Get Data', command=lambda: self.matrixMemory.addMatrix(myMatrix, e.get()))
        button.grid(row=2, column=1)