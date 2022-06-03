from tkinter import *
from tkinter import ttk
import numpy as np
from EigenComputation import Householder

class MatrixMult:
    def __init__(self, root, textArea, matrixMemory):
        self.root = root
        self.operands = []
        self.text = ''
        self.textArea = textArea
        self.matrixMemory = matrixMemory
        self.matrixNamesList, self.dic = self.createOperationDictionary()

    def addMultiplicationWindow(self):
        self.frame = Frame(self.root)

        label = Label(self.frame, text="Select Matrix")
        label.grid(row=0, column=0, columnspan=2)

        var = IntVar()
        self.options = self.getListOfMatrices()
        # print(type(self.options))
        self.comboBox = ttk.Combobox(self.frame, value=self.options)
        self.comboBox.bind("<<ComboboxSelected>>", self.matrixSelected)
        self.comboBox.grid(row=1, column=0, columnspan=2)

        self.functionEntry = Entry(self.frame, width=50)
        self.functionEntry.grid(row=2, column=0, columnspan=2)
        self.functionEntry.config(state='disabled')

        buttonFrame = Frame(self.frame)

        transposeButton = Button(buttonFrame, text='Transpose', width=10, padx=5, pady=5, command=self.transpose)
        transposeButton.grid(row=0, column=3)

        inverseButton = Button(buttonFrame, text='Inverse', width=10, padx=5, pady=5, command=self.inverse)
        inverseButton.grid(row=1, column=3)

        addButton = Button(buttonFrame, text='+', width=10, padx=5, pady=5, command=self.addition)
        addButton.grid(row=2, column=3)

        multButton = Button(buttonFrame, text='*', width=10, padx=5, pady=5, command=self.multiplication)
        multButton.grid(row=3, column=3)

        buttonWrite = Button(buttonFrame, text="Eigen", width=10, padx=5, pady=5, command=lambda: self.printEigen(var.get()))
        buttonWrite.grid(row=4, column=3)

        eqButton = Button(buttonFrame, text='=', width=10, padx=5, pady=5, command=self.equal)
        eqButton.grid(row=4, column=1)
        buttonComa = Button(buttonFrame, text="(", width=10, padx=5, pady=5, command=lambda: self.numberEntered('('))
        buttonComa.grid(row=4, column=0)
        buttonComa = Button(buttonFrame, text=")", width=10, padx=5, pady=5, command=lambda: self.numberEntered(')'))
        buttonComa.grid(row=4, column=2)

        button1 = Button(buttonFrame, text='1', width=10, padx=5, pady=5, command=lambda: self.numberEntered(1))
        button1.grid(row=0, column=0)
        button2 = Button(buttonFrame, text='2', width=10, padx=5, pady=5, command=lambda: self.numberEntered(2))
        button2.grid(row=0, column=1)
        button3 = Button(buttonFrame, text='3', width=10, padx=5, pady=5, command=lambda: self.numberEntered(3))
        button3.grid(row=0, column=2)
        button4 = Button(buttonFrame, text='4', width=10, padx=5, pady=5, command=lambda: self.numberEntered(4))
        button4.grid(row=1, column=0)
        button5 = Button(buttonFrame, text='5', width=10, padx=5, pady=5, command=lambda: self.numberEntered(5))
        button5.grid(row=1, column=1)
        button6 = Button(buttonFrame, text='6', width=10, padx=5, pady=5, command=lambda: self.numberEntered(6))
        button6.grid(row=1, column=2)
        button7 = Button(buttonFrame, text='7', width=10, padx=5, pady=5, command=lambda: self.numberEntered(7))
        button7.grid(row=2, column=0)
        button8 = Button(buttonFrame, text='8', width=10, padx=5, pady=5, command=lambda: self.numberEntered(8))
        button8.grid(row=2, column=1)
        button9 = Button(buttonFrame, text='9', width=10, padx=5, pady=5, command=lambda: self.numberEntered(9))
        button9.grid(row=2, column=2)
        button0 = Button(buttonFrame, text='0', width=10, padx=5, pady=5, command=lambda: self.numberEntered(0))
        button0.grid(row=3, column=1)
        buttonComa = Button(buttonFrame, text=".", width=10, padx=5, pady=5, command=lambda: self.numberEntered('.'))
        buttonComa.grid(row=3, column=0)
        buttonClear = Button(buttonFrame, text="Clear", width=10, padx=5, pady=5, command= self.clearEquation)
        buttonClear.grid(row=3, column=2)

        buttonFrame.grid(row=3, column=0)

        self.frame.grid(row=0, column=1, sticky=N + S + E + W)

    def clearEquation(self):
        self.text = ''
        self.operands = []
        self.printOnTextArea('')

    def numberEntered(self, nmb):
        self.text = self.text + str(nmb)
        self.operands.append(str(nmb))
        # self.number = self.number + str(nmb)
        # self.selectedMatrix = np.transpose(self.selectedMatrix)
        self.printOnTextArea(self.text)

    # def endOfNumber(self):
    #     if self.number != '':

    def printEigen(self, i):
        eigen = Householder.findEigen(self.matrices[i][0])
        sentence = "eigenvalues : " + str(eigen[0]) + '\neigenVectors : ' + str(eigen[1]) + '\n'
        self.textArea.printInOutputArea(sentence)

    def matrixSelected(self, event):
        self.text = self.text + self.allMyMmatrices[self.options.index(self.comboBox.get())][1]
        self.operands.append(self.allMyMmatrices[self.options.index(self.comboBox.get())][1])
        # self.selectedMatrix = self.allMyMmatrices[self.options.index(self.comboBox.get())][0]
        # print(self.selectedMatrix)
        self.printOnTextArea(self.text)

    def transpose(self):
        self.text = self.text + 'Transpose('
        # self.selectedMatrix = np.transpose(self.selectedMatrix)
        self.operands.append('trans')
        self.operands.append('(')
        self.printOnTextArea(self.text)

    def inverse(self):
        self.text = self.text + 'Inverse('
        self.operands.append('inv')
        self.operands.append('(')
        # self.selectedMatrix = np.linalg.inv(self.selectedMatrix)
        self.printOnTextArea(self.text)

    def addition(self):
        self.text = self.text + ' + '
        self.operands.append('+')
        self.printOnTextArea(self.text)

    def multiplication(self):
        self.text = self.text + ' * '
        self.operands.append('*')
        self.printOnTextArea(self.text)

    def equal(self):
        answer = eval(self.evaluate(), self.dic)
        self.textArea.printInOutputArea(str(answer))

    def evaluate(self):
        generalText = ''
        numberID = 0
        print(len(self.operands))
        i = 0
        while i < len(self.operands):
            if i + 2 < len(self.operands):
                if self.operands[i] in self.matrixNamesList and self.operands[i + 1] == '*' and \
                        self.operands[i + 2] in self.matrixNamesList:
                    name = 'index' + str(numberID)
                    generalText = generalText + name
                    self.dic[name] = np.dot(self.dic.get(self.operands[i]), self.dic.get(self.operands[i + 2]))
                    # print(dic[text])
                    numberID += 1
                    i += 3
            if i < len(self.operands):
                if self.operands[i] == "+" or self.operands[i] == "*" or self.operands[i] in self.matrixNamesList \
                        or self.operands[i] == "." or self.operands[i].isdigit()  or self.operands[i] == "(" \
                        or self.operands[i] == ")" or self.operands[i] == "trans" or self.operands[i] == "inv":
                    print('hello', self.operands[i])
                    generalText = generalText + self.operands[i]
                    i += 1
            print(i)
            print(generalText)
        return generalText


    def getListOfMatrices(self):
        self.allMyMmatrices = self.matrixMemory.getMatrices()
        matrixList = []

        for i in range(len(self.allMyMmatrices)):
            text = self.allMyMmatrices[i][1] + ': ' + str(np.shape(self.allMyMmatrices[i][0]))
            matrixList.append((text))
        return matrixList

    def createOperationDictionary(self):
        a = self.matrixMemory.getMatrices()
        b = []
        for i in a:
            b.append((i[1], i[0]))
        dictionary = dict(b)
        matrixName = dictionary.keys()
        print(type(dictionary))
        operationsCommand = {'trans': np.transpose, 'inv': np.linalg.inv}
        dictionary.update(operationsCommand)
        return matrixName, dictionary

    def printOnTextArea(self, textToPrint):
        self.functionEntry.config(state="normal")
        self.functionEntry.delete(0,END)
        self.functionEntry.insert(END, textToPrint)
        self.functionEntry.config(state='disabled')