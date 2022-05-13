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

    def __init__(self, root, row=0, col=0, matrixMemory=None):
        self.entries = []
        self.row = row
        self.col = col
        self.root = root
        self.matrix = []
        self.histrow = 0
        self.histcol = 0
        self.matrixMemory = matrixMemory

    def addMatrixWindow(self):
        """
        Create a new window for the user to enter the matrix of its choice.
        """

        self.window = Toplevel(self.root)

        # self.buttonWrite.grid_remove()
        # self.buttonMatrixFromFile.grid_remove()

        # Creates the labels and the entry boxes for the row and column numbers.

        label1 = Label(self.window, text="row")
        label1.grid(row=0, column=0)
        self.e1 = Entry(self.window, width=10, borderwidth=5)
        self.e1.grid(row=0, column=1)

        label2 = Label(self.window, text="Column")
        label2.grid(row=1, column=0)
        self.e2 = Entry(self.window, width=10, borderwidth=5)
        self.e2.grid(row=1, column=1)

        label3 = Label(self.window, text="Name")
        label3.grid(row=2, column=0)
        self.e3 = Entry(self.window, width=10, borderwidth=5)
        self.e3.grid(row=2, column=1)

        # self.e1.bind_all('<Return>', lambda event: self.updateMatrixWindow)
        # self.e2.bind_all('<Return>', lambda event: self.updateMatrixWindow)

        buttonCreateMatrix = Button(self.window, text="Enter Size", padx=5, pady=5, command=self.updateMatrixWindow)
        buttonCreateMatrix.grid(row=0, column=2, rowspan=3)

    def updateMatrixWindow(self):
        # Enter the column numbers.
        if self.histrow != int(self.e1.get()) or self.histcol != int(self.e2.get()):
            self.histrow = int(self.e1.get())
            self.histcol = int(self.e2.get())
            self.row = int(self.e1.get())
            self.col = int(self.e2.get())

        # Delete all the elements previously present on the grid.
        for label in self.window.grid_slaves():
            if int(label.grid_info()["row"]) > 2:
                label.destroy()

        for c in range(self.col):
            l = Label(self.window, text=str(c))
            l.grid(row=3, column=c + 1)

        # Show the row numbers
        self.entries = []
        for r in range(self.row):
            entries_row = []
            l = Label(self.window, text=str(r))
            l.grid(row=r + 4, column=0)
            # Add the entries for the values.
            for c in range(self.col):
                singleEntry = Entry(self.window, width=5)  # 5 chars
                try:
                    singleEntry.insert('end', self.matrix[r, c])
                except:
                    singleEntry.insert('end', 0)
                singleEntry.grid(row=r + 4, column=c + 1)
                entries_row.append(singleEntry)
            self.entries.append(entries_row)

        saveButton = Button(self.window, text='Get Data', command=self.get_data)
        saveButton.grid(row=self.row + 4, column=0)

        addRowButton = Button(self.window, text='+', command=self.addRow)
        addRowButton.grid(row=self.row + 4, column=1)
        addColButton = Button(self.window, text='+', command=self.addCol)
        addColButton.grid(row=4, column=self.col + 2)

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


    def getMatrixFromFile(self):
        """
        This method is used if the user wants to open a .xcel file containing a matrix.
        Read this file and return the matrix contained into the .xcel file.s
        """
        open_file_loc = filedialog.askopenfilename()
        if open_file_loc != '':
            df = pd.read_excel(open_file_loc, header=None)
            df.values
            # print(df)
            myArray = df.to_numpy()
            # print(myArray)

            windowName = Toplevel(self.root)
            label = Label(windowName, text="Name of the matrix:")
            label.grid(row=0, column=0)
            e = Entry(windowName, width=30, borderwidth=5)
            e.grid(row=1, column=0)

            button = Button(windowName, text='Get Data', command=lambda: self.matrixMemory.addMatrix(myArray, e.get()))
            button.grid(row=2, column=0)

            # self.matrixMemory.addMatrix(myArray, e.get())