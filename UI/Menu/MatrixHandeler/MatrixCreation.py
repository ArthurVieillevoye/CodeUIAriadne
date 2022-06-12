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

    def addMatrixCreationOptions(self):
        """
        Create the window that allows the user to choose how he wants to enter his/her matrix.
        """
        # Clean the frame.
        self.root.grid_slaves()[0].grid_forget()
        self.textArea.deleteAll()

        self.newMatrixFrame = Frame(self.root)

        # Add the buttons for the different creation options.
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

###################################################################
#   SECTION UPLOAD FILE
###################################################################

    def getMatrixFromFile(self):
        """
        This method is used if the user wants to open a .xcel file containing a matrix.
        Read this file and return the matrix contained into the .xcel file.s
        """
        self.clearFrame()

        # Ask to the user the file locatn and return the path to the file.
        open_file_loc = filedialog.askopenfilename()
        if open_file_loc != '' or open_file_loc != '()':
            try:
                # Cast the matrix from excel file to the Ariadne matrices.
                df = pd.read_excel(open_file_loc, header=None)
                myMatrix = FloatDPApproximationMatrix(df.values.tolist(), dp)
                self.nameWindowForUploadedMatrices(myMatrix)
            except:
                try:
                    # Casst the matrix from csv file to the Ariadne matrix.
                    df = pd.read_csv(open_file_loc, header=None, sep=';')
                    myMatrix = FloatDPApproximationMatrix(df.values.tolist(), dp)
                    self.nameWindowForUploadedMatrices(myMatrix)
                except:
                    # If the user entered a wrong file type.
                    self.textArea.printInOutputArea("Error: File is not in the correct format (.csv or .xcel)")

    def nameWindowForUploadedMatrices(self, myMatrix):
        """
        Ask the user for the name of the matrix that he xants to create.
        :param myMatrix: Tha Ariadne matrix extracted from the file.
        """
        # Ask the label and entries to allow the user to enter the name.
        label = Label(self.newMatrixFrame, text="Name of the matrix:")
        label.grid(row=0, column=1)
        e = Entry(self.newMatrixFrame, width=30, borderwidth=5)
        e.grid(row=1, column=1)

        button = Button(self.newMatrixFrame, text='Get Data', command=lambda: self.verifyName(myMatrix, e.get()))
        button.grid(row=2, column=1)

    def verifyName(self, myMatrix, e):
        """
        Verify the correctness of the entered name.
        :param myMatrix: The Ariadne matrix
        :param e: the name of the matrix
        """
        if e == '':
            # If the name is a empty string, throw an error.
            self.textArea.printInOutputArea('Error: name missing')
        else:
            # If the name is correct, save the matrix.
            self.matrixMemory.addMatrix(myMatrix, e)

    ###################################################################
    #   SECTION ENTER MATRIX AS TEXT
    ###################################################################

    def addMatrixTextWindow(self):
        """
        This method is used to allow the user enter its matrix into a python or matlab form.
        """
        self.clearFrame()

        # Enter the labels and the entry that will allow the user to enter its matrix.
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
        """
        Decode the entered matrix to save it.
        Throw an error if the matrix is not in the two correct form.
        :param matrix: The entered matrix in a string format
        :param name: The name of the matrix that the user entered.
        """
        if name == '':
            # Throw an error if the user did not entered a name.
            self.textArea.printInOutputArea('Error: name missing')
        else:
            try:
                # If the user enters its matrix in python form
                self.matrixMemory.addMatrix(FloatDPApproximationMatrix(eval(matrix), dp), name)
            except:
                try:
                    # If the user enters its matrix in matlab form.
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
                    # Throw an error if the matrix has not been entered in a good format.
                    self.textArea.printInOutputArea('You did not enter the matrix in a correct form')

###################################################################
#   SECTION Enter matrix in grid.
###################################################################

    def addMatrixWindow(self):
        """
        Create a new window for the user to enter the matrix of its choice.
        Here, the user enters the matrix by filling it a grid.
        """
        self.clearFrame()

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

        buttonCreateMatrix = Button(self.newMatrixFrame, text="Enter Size", padx=5, pady=5, command=self.getRowAndColumnSize)
        buttonCreateMatrix.grid(row=0, column=3, sticky="ew")

    def getRowAndColumnSize(self):
        """
        This method is called when the user entered a matrix size.
        """
        try:
            # Check if the matrix size is entered correctly, update the matrix size.
            if self.histrow != int(self.e1.get()) or self.histcol != int(self.e2.get()):
                self.histrow = int(self.e1.get())
                self.histcol = int(self.e2.get())
                self.row = int(self.e1.get())
                self.col = int(self.e2.get())
            self.updateMatrixWindow()
        except:
            # Throw an arror if the matrix size is not correct.
            self.textArea.printInOutputArea('Error: The entered size is not an integer.')

    def updateMatrixWindow(self):
        """
        Add the grid to the frame such that the user can enter the matrix.
        """
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
                singleEntry = Entry(self.newMatrixFrame, width=5)

                # Binds the arrows to allow the user to navigate more easily into the grid.
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

        # Add the buttons to the frame.
        saveButton = Button(self.newMatrixFrame, text='Save matrix', padx=5, pady=5, command=self.get_data)
        saveButton.grid(row=2, column=3, sticky="ew")

        addRowButton = Button(self.newMatrixFrame, text='+', command=self.addRow)
        addRowButton.grid(row=self.row, column=5)
        addColButton = Button(self.newMatrixFrame, text='+', command=self.addCol)
        addColButton.grid(row=0, column=self.col + 6)

    def left(self, event):
        """
        This method is calledto change the entry when the user uses the left shortcut
        """
        if self.entryColumns - 1 >= 0:
            self.entryColumns = self.entryColumns - 1
            self.entries[self.entryRow][self.entryColumns].focus()
            print(self.entryRow, self.entryColumns)

    def right(self, event):
        """
        This method is calledto change the entry when the user uses the right shortcut
        """
        if self.entryColumns + 1 <= self.col:
            self.entryColumns = self.entryColumns + 1
            print(self.entryRow, self.entryColumns)
            self.entries[self.entryRow][self.entryColumns].focus()

    def up(self, event):
        """
        This method is calledto change the entry when the user uses the up shortcut
        """
        if self.entryRow - 1 >= 0:
            self.entryRow = self.entryRow - 1
            print(self.entryRow, self.entryColumns)
            self.entries[self.entryRow][self.entryColumns].focus()

    def down(self, event):
        """
        This method is calledto change the entry when the user uses the down shortcut
        """
        if self.entryRow + 1 <= self.row:
            self.entryRow = self.entryRow + 1
            print(self.entryRow, self.entryColumns)
            self.entries[self.entryRow][self.entryColumns].focus()

    def addRow(self):
        """
        Called when the user adds a row using the '+' button.
        Add a row to the display to allowing the user to increase its matrix size while entering its matrix.
        """
        self.entryRow = 0
        self.entryColumns = 0
        self.matrix = self.get_data(True)
        self.row = self.row + 1
        self.updateMatrixWindow()

    def addCol(self):
        """
        Called when the user adds a row using the '+' button
        Add a row to the display to allowing the user to increase its matrix size while entering its matrix.
        """
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
        # Transform the entries into list of list.
        demand = np.zeros((self.row, self.col))
        for r, row in enumerate(self.entries):
            for c, entry in enumerate(row):
                text = entry.get()
                demand[r, c] = float(text)

        demand = FloatDPApproximationMatrix(demand.tolist(), dp)
        if ret:
            return demand
        else:
            # Handels matrix name error.
            if self.e3.get() == '':
                self.textArea.printInOutputArea('Error: name missing')
            else:
                self.matrixMemory.addMatrix(demand, self.e3.get())

    def clearFrame(self):
        """
        Clears the frame.
        """
        for label in self.newMatrixFrame.grid_slaves():
            if int(label.grid_info()["column"]) > 0:
                label.destroy()