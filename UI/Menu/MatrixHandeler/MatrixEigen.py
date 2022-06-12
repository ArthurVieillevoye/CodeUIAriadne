from tkinter import *
from tkinter.ttk import Combobox
import numpy as np
from EigenComputation import Householder
from EigenComputation import IntervalNewtonMethod
from EigenComputation import EigenVecotrs
from pyariadne import *


class MatrixEigen:
    def __init__(self, root, textArea, matrixMemory):
        self.root = root
        self.textArea = textArea
        self.matrixMemory = matrixMemory

    def addEigenWindow(self):
        self.frame = Frame(self.root)

        label1 = Label(self.frame, text="Select symmetric matrix:")
        label1.grid(row=0, column=0)

        var = IntVar()
        self.options = self.getListOfMatrices()
        # print(type(self.options))
        self.comboBox = Combobox(self.frame, value=self.options)
        self.comboBox.bind("<<ComboboxSelected>>", self.matrixSelected)
        self.comboBox.grid(row=1, column=0)

        buttonAllEigen = Button(self.frame, text="All eigen", padx=5, pady=5, width=8,
                                command=self.allEigenButtonActive)
        buttonAllEigen.grid(row=2, column=0)
        buttonAllEigen = Button(self.frame, text="One Eigen", padx=5, pady=5, width=8, command=self.oneEigenButtonActive)
        buttonAllEigen.grid(row=3, column=0, sticky=N)

        self.frame.grid(row=0, column=1, sticky=N + S + E + W)

    def allEigenButtonActive(self):
        try:
            eigenValues, eigenVectors = Householder.findEigenAriadne(self.selectedMatrix)

            self.eigenValuesList = []
            self.eigenVectorList = []
            print("type eigenValues", type(eigenValues))
            for i in range(len(eigenValues)):
                eigenVect, eigenVal = IntervalNewtonMethod.intervalNewtonMethods(Householder.getColumn(i, eigenVectors),
                                                                                 eigenValues[i], self.selectedMatrix)
                self.eigenValuesList.append(eigenVal)
                self.eigenVectorList.append(eigenVect)
            self.displayFoundEigen()
        except:
            self.textArea.printInOutputArea("Error: No matrix selected")


    def displayFoundEigen(self):
        for label in self.frame.grid_slaves():
            if int(label.grid_info()["column"]) > 0:
                label.destroy()

        label = Label(self.frame, text="Found estimate: ")
        label.grid(row=2, column=1)

        var = IntVar()
        window = Frame(self.frame)
        for i in range(len(self.eigenValuesList)):
            text = str(self.eigenValuesList[i]) + " : " + str(self.eigenVectorList[i])
            if len(text) > 65:
                text = text[0:65] + " ..."
            Radiobutton(window, text=text, padx=20, variable=var, value=i).pack(anchor=W)

            window.grid(row=3, column=1, rowspan=50, sticky=N + S + E + W)

        buttonCopy = Button(self.frame,  text="copy bound", width=11, padx=5, pady=5, command=lambda: self.gtc(var.get(), False))
        buttonCopy.grid(row=3, column=2)
        buttonPrint = Button(self.frame, text="Print bound", width=11, padx=5, pady=5, command=lambda: self.printEstimate(var.get(), False))
        buttonPrint.grid(row=4, column=2)
        buttonMiddle = Button(self.frame, text="copy mid-point", width=11, padx=5, pady=5, command=lambda: self.gtc(var.get(), True))
        buttonMiddle.grid(row=5, column=2)
        buttonMiddle = Button(self.frame, text="Print mid-point", width=11, padx=5, pady=5, command=lambda: self.printEstimate(var.get(), True))
        buttonMiddle.grid(row=6, column=2)

    def printEstimate(self, i, midPoint):
        if midPoint:
            sentence = repr(cast_exact(self.eigenValuesList[i])) + " : " + repr(cast_exact(self.eigenVectorList[i])) + '\n'
        else:
            sentence = repr(self.eigenValuesList[i]) + " : " + repr(self.eigenVectorList[i]) + '\n'
        self.textArea.printInOutputArea(sentence)


    def gtc(self, i, midPoint):
        self.root.clipboard_clear()
        if midPoint:
            selectedEigen = (cast_exact(self.eigenValuesList[i]), cast_exact(self.eigenVectorList[i]))
        else:
            selectedEigen = (self.eigenValuesList[i], self.eigenVectorList[i])

        self.root.clipboard_append(selectedEigen)


    def oneEigenButtonActive(self):
        try:
            self.selectedMatrix.row_size()
            for label in self.frame.grid_slaves():
                if int(label.grid_info()["column"]) > 0:
                    label.destroy()

            label = Label(self.frame, text = "eigenvalue estimate (optional): ")
            label.grid(row=2, column=1)
            self.entry1 = Entry(self.frame, width=30)
            # entry.insert(END, "1")
            self.entry1.grid(row=3, column=1)
            label = Label(self.frame, text="Eigenvector estimate (optional): ")
            label.grid(row=4, column=1)
            self.entry2 = Entry(self.frame, width=30)
            # entry.insert(END, "1")
            self.entry2.grid(row=5, column=1)

            computerEigenButton = Button(self.frame, text="get Eigen", padx=5, pady=5, command= self.getEigenComputed)
            computerEigenButton.grid(row=6, column=1)
        except:
            self.textArea.printInOutputArea("Error: No matrix selected")

    def getEigenComputed(self):
        if self.entry1.get() !='' and self.entry2.get() !='':
            print("hello", self.entry1.get())
            eigenValEstimate = FloatDPApproximation(eval(self.entry1.get()), dp)
            eigenVectEstimate = self.decodeEnteredMatrix(self.entry2.get())
            eigenVect, eigenVal = IntervalNewtonMethod.intervalNewtonMethods(eigenVectEstimate, eigenValEstimate, self.selectedMatrix)
            self.eigenVectorList = [eigenVect]
            self.eigenValuesList = [eigenVal]
            self.displayFoundEigen()

        else:
            eigenValEstimate, eigenVectEstimate = EigenVecotrs.power_methods(self.selectedMatrix)
            eigenVect, eigenVal = IntervalNewtonMethod.intervalNewtonMethods(eigenVectEstimate, eigenValEstimate, self.selectedMatrix)
            self.eigenVectorList = [eigenVect]
            self.eigenValuesList = [eigenVal]
            self.displayFoundEigen()


    def decodeEnteredMatrix(self, matrix):
        try:
            return FloatDPApproximationMatrix(myMatrix, dp)
        except:
            try:
                myMatrix = []
                matrix = matrix.replace("[", "")
                matrix = matrix.replace("]", "")
                matrix = matrix.replace(" ", "")

                matrix = matrix.split(';')
                for el in matrix:
                    listTmp = '[' + el + ']'
                    myMatrix.append(eval(listTmp))
                print(myMatrix)
                return FloatDPApproximationMatrix(myMatrix, dp)
            except:
                self.textArea.printInOutputArea('You did not enter the eigenvector approximation in a correct form')


    def matrixSelected(self, event):
        for label in self.frame.grid_slaves():
            if int(label.grid_info()["column"]) > 0:
                label.destroy()

        self.selectedMatrix = self.allMyMmatrices[self.options.index(self.comboBox.get())][0]
        self.textArea.addMatrixDisplay(self.frame, text=str(self.selectedMatrix))
        print(self.selectedMatrix)


    def getListOfMatrices(self):
        self.allMyMmatrices = self.matrixMemory.getMatrices()
        matrixList = []

        for i in range(len(self.allMyMmatrices)):
            text = self.allMyMmatrices[i][1] + ': (' + str(self.allMyMmatrices[i][0].row_size()) + " " + \
                   str(self.allMyMmatrices[i][0].column_size()) + ")"
            matrixList.append((text))
        return matrixList