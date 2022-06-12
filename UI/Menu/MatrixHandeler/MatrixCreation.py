from tkinter import *
import numpy as np
# import pandas as pd
from tkinter import filedialog
from pyariadne import *


class MatrixCreationWindow:
    """
    This class contains all the information for the input of a matrix into the file.
    It contains 2 matrix creation element: One where you can write it yourself and another one where you can upload
    the matrix from a file.
    """

    def __init__(self, root, textArea, matrixMemory=None):
        self.entries = []
        self.row = 0
        self.col = 0
        self.root = root
        self.matrix = []
        self.histrow = 0
        self.histcol = 0
        self.entryRow = 0
        self.entryColumns = 0
        self.textArea = textArea
        self.matrixMemory = matrixMemory

    def clearFrame(self):
        for label in self.newMatrixFrame.grid_slaves():
            if int(label.grid_info()["column"]) > 0:
                label.destroy()

    def addMatrixWindow(self):
        """
        Create a new window for the user to enter the matrix of its choice.
        """

        self.clearFrame()

        # self.buttonWrite.grid_remove()
        # self.buttonMatrixFromFile.grid_remove()

        # Creates the labels and the entry boxes for the row and column numbers.

        label1 = Label(self.newMatrixFrame, text="row")
        label1.grid(row=0, column=1)
        self.e1 = Entry(self.newMatrixFrame, width=10, borderwidth=5)
        self.e1.grid(row=0, column=2)

        label2 = Label(self.newMatrixFrame, text="Column")
        label2.grid(row=1, column=1)
        self.e2 = Entry(self.newMatrixFrame, width=10, borderwidth=5)
        self.e2.grid(row=1, column=2)

        label3 = Label(self.newMatrixFrame, text="Name")
        label3.grid(row=2, column=1)
        self.e3 = Entry(self.newMatrixFrame, width=10, borderwidth=5)
        self.e3.grid(row=2, column=2)

        # self.e1.bind_all('<Return>', lambda event: self.updateMatrixWindow)
        # self.e2.bind_all('<Return>', lambda event: self.updateMatrixWindow)

        buttonCreateMatrix = Button(self.newMatrixFrame, text="Enter Size", padx=5, pady=5, command=self.getRowAndColumnSize)
        buttonCreateMatrix.grid(row=0, column=3, sticky="ew")

    def getRowAndColumnSize(self):
        # Enter the column numbers.
        try:
            if self.histrow != int(self.e1.get()) or self.histcol != int(self.e2.get()):
                self.histrow = int(self.e1.get())
                self.histcol = int(self.e2.get())
                self.row = int(self.e1.get())
                self.col = int(self.e2.get())
            self.updateMatrixWindow()
        except:
            self.textArea.printInOutputArea('Error: The entered size is not an integer.')

    def updateMatrixWindow(self):

        print(self.row, self.col)
        # Delete all the elements previously present on the grid.
        for label in self.newMatrixFrame.grid_slaves():
            if int(label.grid_info()["column"]) > 3:
                label.destroy()

        # Show the column numbers
        for c in range(self.col):
            l = Label(self.newMatrixFrame, text=str(c))
            l.grid(row=0, column=c + 5)

        # Show the row numbers
        self.entries = []
        for r in range(self.row):
            entries_row = []
            l = Label(self.newMatrixFrame, text=str(r))
            l.grid(row=r, column=4)
            # Add the entries for the values.
            for c in range(self.col):
                singleEntry = Entry(self.newMatrixFrame, width=5)  # 5 chars
                # singleEntry.bind("<Button-1>", lambda e: self.updateIndexes(e, singleEntry))
                singleEntry.bind("<Control-Left>", lambda e: self.left(e))
                singleEntry.bind("<Control-Right>", lambda e: self.right(e))
                singleEntry.bind("<Control-Up>", lambda e: self.up(e))
                singleEntry.bind("<Control-Down>", lambda e: self.down(e))
                try:
                    singleEntry.insert('end', self.matrix[r, c])
                except:
                    singleEntry.insert('end', 0)
                singleEntry.grid(row=r, column=c + 5)
                entries_row.append(singleEntry)
            self.entries.append(entries_row)

        saveButton = Button(self.newMatrixFrame, text='Save matrix', padx=5, pady=5, command=self.get_data)
        saveButton.grid(row=2, column=3, sticky="ew")

        addRowButton = Button(self.newMatrixFrame, text='+', command=self.addRow)
        addRowButton.grid(row=self.row, column=5)
        addColButton = Button(self.newMatrixFrame, text='+', command=self.addCol)
        addColButton.grid(row=0, column=self.col + 6)

    def left(self, event):
        if self.entryColumns - 1 >= 0:
            self.entryColumns = self.entryColumns - 1
            self.entries[self.entryRow][self.entryColumns].focus()
            print(self.entryRow, self.entryColumns)

    def right(self, event):
        if self.entryColumns + 1 <= self.col:
            self.entryColumns = self.entryColumns + 1
            print(self.entryRow, self.entryColumns)
            self.entries[self.entryRow][self.entryColumns].focus()

    def up(self, event):
        if self.entryRow - 1 >= 0:
            self.entryRow = self.entryRow - 1
            print(self.entryRow, self.entryColumns)
            self.entries[self.entryRow][self.entryColumns].focus()

    def down(self, event):
        if self.entryRow + 1 <= self.row:
            self.entryRow = self.entryRow + 1
            print(self.entryRow, self.entryColumns)
            self.entries[self.entryRow][self.entryColumns].focus()

    def addRow(self):
        self.entryRow = 0
        self.entryColumns = 0
        self.matrix = self.get_data(True)
        self.row = self.row + 1
        self.updateMatrixWindow()

    def addCol(self):
        self.entryRow = 0
        self.entryColumns = 0
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

        demand = FloatDPApproximationMatrix(demand.tolist(), dp)
        if ret:
            print(demand)
            return demand
        else:
            if self.e3.get() == '':
                self.textArea.printInOutputArea('Error: name missing')
            else:
                self.matrixMemory.addMatrix(demand, self.e3.get())

    def addMatrixTextWindow(self):
        self.clearFrame()

        label1 = Label(self.newMatrixFrame, text='Enter your matrix in python or matlab form')
        label1.grid(row=0, column=1, columnspan=2)

        label2 = Label(self.newMatrixFrame, text='Matrix: ')
        label2.grid(row=1, column=1)
        matrixEntry = Entry(self.newMatrixFrame, width=100)
        matrixEntry.grid(row=1, column=2)

        label = Label(self.newMatrixFrame, text="Name of the matrix:")
        label.grid(row=2, column=1)
        entryName = Entry(self.newMatrixFrame, width=50)
        entryName.grid(row=2, column=2, sticky=W)

        button = Button(self.newMatrixFrame, text='save Matrix', padx=5, pady=5,
                        command=lambda: self.decodeEnteredMatrix(matrixEntry.get(), entryName.get()))
        button.grid(row=3, column=1)

    def decodeEnteredMatrix(self, matrix, name):
        if name == '':
            self.textArea.printInOutputArea('Error: name missing')
        else:
            passed = True
            try:
                self.matrixMemory.addMatrix(FloatDPApproximationMatrix(eval(matrix), dp), name)
            except:
                passed = False
            try:
                if not passed:
                    passed = True
                    myMatrix = []
                    matrix = matrix.replace("[", "")
                    matrix = matrix.replace("]", "")
                    matrix = matrix.replace(" ", "")

                    matrix = matrix.split(';')
                    for el in matrix:
                        listTmp = '[' + el + ']'
                        myMatrix.append(eval(listTmp))
                    print(myMatrix)
                    self.matrixMemory.addMatrix(FloatDPApproximationMatrix(myMatrix, dp), name)
            except:
                passed = False

            if not passed:
                self.textArea.printInOutputArea('You did not enter the matrix in a correct form')

    def getMatrixFromFile(self):
        """
        This method is used if the user wants to open a .xcel file containing a matrix.
        Read this file and return the matrix contained into the .xcel file.s
        """
        self.clearFrame()
        
        open_file_loc = filedialog.askopenfilename()
        if open_file_loc != '' or open_file_loc != '()':
            print(open_file_loc)
            try:
                df = pd.read_excel(open_file_loc, header=None)
                myMatrix = FloatDPApproximationMatrix(df.values.tolist(), dp)
                self.nameWindowForUploadedMatrices(myMatrix)
            except:
                try:
                    df = pd.read_csv(open_file_loc, header=None, sep=';')
                    myMatrix = FloatDPApproximationMatrix(df.values.tolist(), dp)
                    self.nameWindowForUploadedMatrices(myMatrix)
                except:
                    self.textArea.printInOutputArea("Error: File is not in the correct format (.csv or .xcel)")

    def nameWindowForUploadedMatrices(self, myMatrix):
        label = Label(self.newMatrixFrame, text="Name of the matrix:")
        label.grid(row=0, column=1)
        e = Entry(self.newMatrixFrame, width=30, borderwidth=5)
        e.grid(row=1, column=1)

        button = Button(self.newMatrixFrame, text='Get Data', command=lambda: self.verifyName(myMatrix, e.get()))
        button.grid(row=2, column=1)

    def verifyName(self, myMatrix, e):
        if e == '':
            self.textArea.printInOutputArea('Error: name missing')
        else:
            self.matrixMemory.addMatrix(myMatrix, e)




    # def bMatrixFromFile(self):
    #     """
    #     Call the matrixCreation object.
    #     Allow the user choose an excel file containing a matrix.
    #     """
    #     m = MatrixCreation.MatrixCreationWindow(self.newMatrixFrame,self.textArea, matrixMemory=self.matrixMemory)
    #     m.getMatrixFromFile()
    #
    # def bMatrixEnter(self):
    #     """
    #     This methods creates the window on which the user can enter the size of the matrix he wants to enter.
    #     """
    #     m = MatrixCreation.MatrixCreationWindow(self.newMatrixFrame, textArea=self.textArea, matrixMemory=self.matrixMemory)
    #     m.addMatrixWindow()
    #
    # def bMatrixWrite(self):
    #     # self.buttonEnter.grid_remove()
    #     # self.buttonWrite.grid_remove()
    #     # self.buttonMatrixFromFile.grid_remove()
    #     m = MatrixCreation.MatrixCreationWindow(self.newMatrixFrame, textArea=self.textArea, matrixMemory=self.matrixMemory)
    #     m.addMatrixTextWindow()


    def addMatrixCreationOptions(self):
        """
        Create the window that allows the user to choose how he wants to enter his/her matrix.
        """
        self.root.grid_slaves()[0].grid_forget()
        self.textArea.deleteAll()

        self.newMatrixFrame = Frame(self.root)
        # self.newWindow.geometry("200x200")
        self.buttonEnter = Button(self.newMatrixFrame, text="Enter Matrix", padx=5, pady=5,
                                  command=self.addMatrixWindow)
        self.buttonEnter.grid(row=0, column=0, sticky="new")

        self.buttonWrite = Button(self.newMatrixFrame, text="Write Matrix", padx=5, pady=5,
                                  command=self.addMatrixTextWindow)
        self.buttonWrite.grid(row=1, column=0, sticky="new")

        self.buttonMatrixFromFile = Button(self.newMatrixFrame, text="Upload Matrix", padx=5, pady=5,
                                           command=self.getMatrixFromFile)
        self.buttonMatrixFromFile.grid(row=2, column=0, sticky="new")

        self.newMatrixFrame.grid(row=0, column=1, sticky=N + S + E + W)