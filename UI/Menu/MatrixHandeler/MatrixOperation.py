from tkinter import *
from tkinter import ttk
import numpy as np
from EigenComputation import Householder

class MatrixMult:
    def __init__(self, root, matrixSelector, textArea, matrixMemory):
        self.root = root
        self.matrixSelector = matrixSelector
        self.operation = ''
        self.text = ''
        self.previousText = ''
        self.textArea = textArea
        self.previousMatrix = []
        self.matrixMemory = matrixMemory

    def addMultiplicationWindow(self):
        frame = Frame(self.root)

        label = Label(frame, text="Select Matrix")
        label.grid(row=0, column=0, columnspan=2)

        var = IntVar()
        self.options = self.getListOfMatrices()
        # print(type(self.options))
        self.comboBox = ttk.Combobox(frame, value=self.options)
        self.comboBox.bind("<<ComboboxSelected>>", self.matrixSelected)
        self.comboBox.grid(row=1, column=0, columnspan=2)

        self.functionEntry = Entry(frame, width=50)
        self.functionEntry.grid(row=2, column=0, columnspan=2)
        self.functionEntry.config(state='disabled')

        transposeButton = Button(frame, text='Transpose', width=10, padx=5, pady=5, command=self.transpose)
        transposeButton.grid(row=3, column=0)

        inverseButton = Button(frame, text='Inverse', width=10, padx=5, pady=5, command=self.inverse)
        inverseButton.grid(row=3, column=1)

        addButton = Button(frame, text='+', width=10, padx=5, pady=5, command=self.addition)
        addButton.grid(row=4, column=0)

        multButton = Button(frame, text='*', width=10, padx=5, pady=5, command=self.multiplication)
        multButton.grid(row=4, column=1)

        buttonWrite = Button(frame, text="Eigen", width=10, padx=5, pady=5, command=lambda: self.printEigen(var.get()))
        buttonWrite.grid(row=5, column=0)

        eqButton = Button(frame, text='=', width=10, padx=5, pady=5, command=self.equal)
        eqButton.grid(row=5, column=1)


        frame.grid(row=0, column=1, sticky=N + S + E + W)

    def printEigen(self, i):
        eigen = Householder.findEigen(self.matrices[i][0])
        sentence = "eigenvalues : " + str(eigen[0]) + '\neigenVectors : ' + str(eigen[1]) + '\n'
        self.textArea.printInOutputArea(sentence)

    def matrixSelected(self, event):
        self.text = self.allMyMmatrices[self.options.index(self.comboBox.get())][1]
        self.selectedMatrix = self.allMyMmatrices[self.options.index(self.comboBox.get())][0]
        print(self.selectedMatrix)
        self.printOnTextArea(self.previousText + self.text)

    def transpose(self):
        self.text = 'T(' + self.text +')'
        self.selectedMatrix = np.transpose(self.selectedMatrix)
        self.printOnTextArea(self.previousText + self.text)

    def inverse(self):
        self.text = 'I(' + self.text + ')'
        self.selectedMatrix = np.linalg.inv(self.selectedMatrix)
        self.printOnTextArea(self.previousText + self.text)

    def addition(self):
        self.previousMatrix = self.selectedMatrix
        self.selectedMatrix = []
        self.text = self.text + ' + '
        self.previousText = self.text
        self.text = ''
        self.operation = 'add'
        self.printOnTextArea(self.previousText + self.text)

    def multiplication(self):
        self.previousMatrix = self.selectedMatrix
        self.selectedMatrix = []
        self.text = self.text + ' * '
        self.previousText = self.text
        self.text = ''
        self.operation = 'mult'
        self.printOnTextArea(self.previousText + self.text)

    def equal(self):
        if self.operation == 'add':
            answer = self.previousMatrix + self.selectedMatrix
        elif self.operation == 'mult':
            answer = np.dot(self.previousMatrix, self.selectedMatrix)
        else:
            answer = self.selectedMatrix
        print(answer)

        label = Label(self.newWindow, text="Name: ")
        label.grid(row=6, column=0)
        e = Entry(self.newWindow)
        e.grid(row=6, column=1)

        saveButton = Button(self.newWindow, text='save', width=10, padx=5, pady=5,
                            command=lambda: self.matrixMemory.addMatrix(answer, e.get()))
        saveButton.grid(row=7, column=0, columnspan=2)

        return answer


    def getListOfMatrices(self):
        self.allMyMmatrices = self.matrixSelector.getMatrices()
        matrixList = []

        for i in range(len(self.allMyMmatrices)):
            text = self.allMyMmatrices[i][1] + ': ' + str(np.shape(self.allMyMmatrices[i][0]))
            matrixList.append((text))
        return matrixList

    def printOnTextArea(self, textToPrint):
        self.functionEntry.config(state="normal")
        self.functionEntry.delete(0,END)
        self.functionEntry.insert(END, textToPrint)
        self.functionEntry.config(state='disabled')