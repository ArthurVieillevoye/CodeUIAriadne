from tkinter import *
from tkinter.ttk import Combobox
import numpy as np


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
                                command=lambda: self.allEigenButtonActive(np.array([[1,2,3],[4,5,6],[7,8,9]]), [10,11,12]))
        buttonAllEigen.grid(row=2, column=0)
        buttonAllEigen = Button(self.frame, text="One Eigen", padx=5, pady=5, width=8, command=self.oneEigenButtonActive)
        buttonAllEigen.grid(row=3, column=0, sticky=N)

        self.frame.grid(row=0, column=1, sticky=N + S + E + W)

    def allEigenButtonActive(self, eigenVectors, eigenValues):
        try:
            for label in self.frame.grid_slaves():
                if int(label.grid_info()["column"]) > 0:
                    label.destroy()

            label = Label(self.frame, text="Found estimate: ")
            label.grid(row=2, column=1)

            var = IntVar()
            window = Frame(self.frame)
            for i in range(len(eigenValues)):
                text = str(eigenValues[i]) + " : " + str(eigenVectors[:,i])
                Radiobutton(window, text=text, padx=20, variable=var, value=i).pack(anchor=W)

            window.grid(row=3, column=1, rowspan=50, sticky=N + S + E + W)

            buttonCopy = Button(self.frame,  text="copy bound", width=8, padx=5, pady=5)
            buttonCopy.grid(row=3, column=2)
            buttonPrint = Button(self.frame, text="Print bound", width=8, padx=5, pady=5)
            buttonPrint.grid(row=4, column=2)
            buttonMiddle = Button(self.frame, text="Get mid-point", width=8, padx=5, pady=5)
            buttonMiddle.grid(row=5, column=2)
        except:
            self.textArea.printInOutputArea("Error: No matrix selected")

    def oneEigenButtonActive(self):
        for label in self.frame.grid_slaves():
            if int(label.grid_info()["column"]) > 0:
                label.destroy()

        label = Label(self.frame, text = "lambda estimate (optional): ")
        label.grid(row=2, column=1)
        entry = Entry(self.frame, width=30)
        entry.insert(END, "1")
        entry.grid(row=3, column=1)

        computerEigenButton = Button(self.frame, text="get Eigen", padx=5, pady=5)
        computerEigenButton.grid(row=4, column=1)

        self.allEigenButtonActive(np.array([[1],[4],[7]]),[10])


    def matrixSelected(self, event):
        self.selectedMatrix = self.allMyMmatrices[self.options.index(self.comboBox.get())][0]
        self.textArea.addMatrixDisplay(self.frame, text="helloEigen")
        print(self.selectedMatrix)


    def getListOfMatrices(self):
        self.allMyMmatrices = self.matrixMemory.getMatrices()
        matrixList = []

        for i in range(len(self.allMyMmatrices)):
            text = self.allMyMmatrices[i][1] + ': ' + str(np.shape(self.allMyMmatrices[i][0]))
            matrixList.append((text))
        return matrixList