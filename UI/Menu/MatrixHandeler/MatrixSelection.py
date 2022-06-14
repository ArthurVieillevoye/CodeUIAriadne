import math
from tkinter import *
import numpy as np
from pyariadne import *


class Matrices:
    """
    This class handles the matrix memory and those matrices managment.
    """
    def __init__(self, root, textArea):
        self.matrices = self.readDatabaseFromFile()
        self.root = root
        self.frame = Frame(self.root)
        self.textArea = textArea
        self.histrow = 0
        self.histcol = 0

    def seeMatrices(self):
        """
        Display all e matrices and add the different option for the user.
        """
        var = IntVar()
        window = Frame(self.frame)

        # Add the matrices in a nice way to the frame.
        for i in range(len(self.matrices)):
            text = self.matrices[i][1] + ': (' + str(self.matrices[i][0].column_size()) + ' ' + str(self.matrices[i][0].row_size()) + ')'
            Radiobutton(window, text=text, padx=20, variable=var, value=i, command= lambda: self.radioButtonSelected(var.get())).pack(anchor=W)

        # Add the buttons for the different users options.
        buttonSee = Button(window, text="Modify Matrix", width=18, padx=5, pady=5,
                           command=lambda: self.showSelectedMatrix(var.get()))
        buttonSee.pack(anchor=W)
        buttonPrecision = Button(window, text="Modify Matrix Precision", width=18, padx=5, pady=5,
                            command=lambda: self.modifyPrecision(var.get()))
        buttonPrecision.pack(anchor=W)
        buttonSee = Button(window, text="Print Matrix", width=18, padx=5, pady=5,
                           command=lambda: self.printMatrix(var.get()))
        buttonSee.pack(anchor=W)
        buttonCopy = Button(window, text="Copy Matrix", width=18, padx=5, pady=5, command=self.gtc)
        buttonCopy.pack(anchor=W)
        buttonCopy = Button(window, text="Delete Matrix", width=18, padx=5, pady=5,
                            command=lambda: self.deleteMatrix(var.get()))
        buttonCopy.pack(anchor=W)

        self.radioButtonSelected(var.get())

        window.grid(row=0, column=0, sticky=N + S + E + W)
        self.frame.grid(row=0, column=1, sticky=N + S + E + W)

    def showSelectedMatrix(self, i):
        """
        Allow the user to modify one of the matrix he has already entered.
        :param i: The index of the selected matrix.
        """
        self.clearFrame()

        window = Frame(self.frame)

        m = self.selectedMatrix.row_size()
        n = self.selectedMatrix.column_size()
        if self.histrow != int(m) or self.histcol != int(n):
            self.histrow = int(m)
            self.histcol = int(n)
            self.row = int(m)
            self.col = int(n)

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
                    singleEntry.insert('end', self.selectedMatrix[r, c])
                except:
                    singleEntry.insert('end', 0)
                singleEntry.grid(row=r, column=c + 1)
                entries_row.append(singleEntry)
            self.entries.append(entries_row)

        saveButton = Button(window, text='save changes', padx=5, pady=5, command=lambda: self.get_data(i))
        saveButton.grid(row=self.row + 1, column=1, sticky="ew")
        window.grid(row=0, column=1, sticky=N + S + E + W)

    def modifyPrecision(self, i):
        """
        This matrix is used to allow the user to modify the precision of one of its matrix.
        :param i: The selected matrix.
        """
        self.clearFrame()
        window = Frame(self.frame)

        # Add the precisions options for the user
        label1 = Label(window, text="precision (in decimal places): ")
        label1.grid(row=0, column=0, padx=5, pady=5)
        decimalEntry = Entry(window, width=25)
        decimalEntry.grid(row=0, column=1, padx=5, pady=5, sticky=N +W)

        label1 = Label(window, text="precision (in digit number): ")
        label1.grid(row=1, column=0, padx=5, pady=5)
        digitEntry = Entry(window, width=25)
        digitEntry.grid(row=1, column=1, padx=5, pady=5, sticky=N + W)

        buttonSave = Button(window, text='Save Changes', padx=5, pady=5, command=lambda: self.saveNewPrecision(i, digitEntry))
        buttonSave.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        window.grid(row=0, column=1, sticky=N + S + E + W)

    def saveNewPrecision(self, selectedMatrix, digitEntry):
        selectedMatrix = self.matrices.pop(i)

        newPrecision = math.ceil(eval(digitEntry.get()))
        matrix = repr(selectedMatrix[0])
        matrix = matrix.replace(str(selectedMatrix[0][0,0].precision()), "mp("+str(newPrecision)+")")

        self.addMatrix(eval(matrix), selectedMatrix[1])
        self.textArea.printInOutputArea("Modification in matrix \"" + selectedMatrix[1] + "\" saved")
        self.seeMatrices()

    def printMatrix(self, i):
        """
        Print the selected matrix on the outputTextArea.
        :param i: the index of the selected matrix.
        """
        self.clearFrame()

        sentence = "Matrix : " + self.matrices[i][1] + " = " + repr(self.matrices[i][0]) + '\n'
        self.textArea.printInOutputArea(sentence)
        self.textArea.addMatrixDisplay(self.frame, str(self.selectedMatrix))

    def gtc(self):
        """
        Allow the user to copy the selected estimate. (put the estimate into the clipboard).
        """
        self.clearFrame()

        self.root.clipboard_clear()
        self.root.clipboard_append(repr(self.selectedMatrix))
        self.textArea.addMatrixDisplay(self.frame, str(self.selectedMatrix))

    def deleteMatrix(self, i):
        """
        Delete the selected matrix from the database.
        :param i: the index of the selected matrix/
        """
        self.matrices.pop(i)
        self.writeOnFile(self.matrices)
        for el in self.frame.grid_slaves():
            el.grid_forget()

        self.seeMatrices()

    def getMatrices(self):
        return self.matrices

    def writeOnFile(self, lst):
        """
        Used to save the created matrix on a text file.
        :param lst: the list of the matrices.
        """
        with open('UI/MatrixDatabase.txt', 'w') as fp:
            fp.truncate(0)

            fp.write('\n'.join('{};{}'.format(repr(x[0]), x[1]) for x in lst))
            fp.close()

    def readDatabaseFromFile(self):
        """
        Read the saved matrices from the file in order for the user to access them.
        :return: the list of Ariadne's form matrices.
        """
        mylist = []
        try:
            with open('UI/MatrixDatabase.txt') as f:
                for i in f:
                    a, b = i.split(';')
                    b = b.replace('\n', '')
                    mylist.append((eval(a), b))
                f.close()
        except:
            pass
        return mylist

    def addMatrix(self, matrix, name=''):
        """
        Add matrix to the database and to the list of already existing matrices.
        :param matrix: the new matrix
        :param name: the name of the matrix.
        """
        if name != '':
            self.matrices.append((matrix, name))
            self.writeOnFile(self.matrices)
        else:
            self.textArea.printInOutputArea('Error: Your matrix must have a name')

    def get_data(self, i, ret=False):
        """
        Save the changes made in the modifyMatrix section.
        :param i: the index of the modified matrix.
        :param ret: boolean to know if the matrix needs to be returned of not.
        :return: the matrix if asked.
        """
        selectedMatrix = self.matrices.pop(i)

        demand = np.zeros((self.row, self.col))
        for r, row in enumerate(self.entries):
            for c, entry in enumerate(row):
                text = entry.get()
                demand[r, c] = float(text)

        pr = precision(128)
        demand = FloatMPApproximationMatrix(demand.tolist(), pr)
        if ret:
            return demand
        else:
            self.addMatrix(demand, selectedMatrix[1])
            self.textArea.printInOutputArea("Modification in matrix \""+ selectedMatrix[1] + "\" saved")
        self.seeMatrices()

    def radioButtonSelected(self, i):
        """
        Display the selected matrix such that the user can see it.
        :param i: index of the selected matrix.
        """
        self.clearFrame()

        self.selectedMatrix = self.matrices[i][0]
        self.textArea.addMatrixDisplay(self.frame, str(self.selectedMatrix))

    def clearFrame(self):
        """
        Clears the frame.
        """
        for label in self.frame.grid_slaves():
            if int(label.grid_info()["column"]) > 0:
                label.destroy()