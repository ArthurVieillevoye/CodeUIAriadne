from tkinter import *
import numpy as np
import pandas as pd
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
        self.textArea = textArea
        self.matrixMemory = matrixMemory

    def addMatrixWindow(self):
        """
        Create a new window for the user to enter the matrix of its choice.
        """

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

        buttonCreateMatrix = Button(self.root, text="Enter Size", padx=5, pady=5, command=self.updateMatrixWindow)
        buttonCreateMatrix.grid(row=0, column=3, sticky="ew")

    def updateMatrixWindow(self):
        # Enter the column numbers.
        if self.histrow != int(self.e1.get()) or self.histcol != int(self.e2.get()):
            self.histrow = int(self.e1.get())
            self.histcol = int(self.e2.get())
            self.row = int(self.e1.get())
            self.col = int(self.e2.get())

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
                singleEntry = Entry(self.root, width=5)  # 5 chars
                try:
                    singleEntry.insert('end', self.matrix[r, c])
                except:
                    singleEntry.insert('end', 0)
                singleEntry.grid(row=r, column=c + 5)
                entries_row.append(singleEntry)
            self.entries.append(entries_row)

        saveButton = Button(self.root, text='Save matrix', padx=5, pady=5, command=self.get_data)
        saveButton.grid(row=2, column=3, sticky="ew")

        addRowButton = Button(self.root, text='+', command=self.addRow)
        addRowButton.grid(row=self.row, column=5)
        addColButton = Button(self.root, text='+', command=self.addCol)
        addColButton.grid(row=0, column=self.col + 6)

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

        demand = FloatDPApproximationMatrix(demand.tolist(), dp)
        if ret:
            print(demand)
            return demand
        else:
            print(demand)
            self.matrixMemory.addMatrix(demand, self.e3.get())


    def getMatrixFromFile(self):
        """
        This method is used if the user wants to open a .xcel file containing a matrix.
        Read this file and return the matrix contained into the .xcel file.s
        """
        open_file_loc = filedialog.askopenfilename()
        if open_file_loc != '' or open_file_loc != '()':
            print(open_file_loc)
            try:
                df = pd.read_excel(open_file_loc, header=None)
                myMatrix = FloatDPApproximationMatrix(df.values.tolist(), dp)
                self.nameWindowForUploadedMatrices(myMatrix)
            except:
                try:
                    print('hello')
                    df = pd.read_csv(open_file_loc, header=None, sep=';')
                    print('df: ', df)
                    myMatrix = FloatDPApproximationMatrix(df.values.tolist(), dp)
                    self.nameWindowForUploadedMatrices(myMatrix)
                except:
                    self.textArea.printInOutputArea("Error: File is not in the correct format (.csv or .xcel)")

    def nameWindowForUploadedMatrices(self, myMatrix):

        frame = Frame(self.root)

        label = Label(frame, text="Name of the matrix:")
        label.grid(row=0, column=0)
        e = Entry(frame, width=30, borderwidth=5)
        e.grid(row=1, column=0)

        button = Button(frame, text='Get Data', command=lambda: self.matrixMemory.addMatrix(myArray, e.get()))
        button.grid(row=2, column=0)

        frame.grid(row=0, column=1)