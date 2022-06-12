from tkinter import *
from tkinter import ttk
import numpy as np
from EigenComputation import Householder
from pyariadne import *

class MatrixMult:
    """
    This class allow the user tor perform basic matrix operation.
    """
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

        # Add the matrixes into the comboboxes.
        self.options = self.getListOfMatrices()
        # print(type(self.options))
        self.comboBox = ttk.Combobox(self.frame, value=self.options)
        self.comboBox.bind("<<ComboboxSelected>>", self.matrixSelected)
        self.comboBox.grid(row=1, column=0, columnspan=2)

        # This entry displays the formulae that the user is entering.
        self.functionEntry = Entry(self.frame, width=50)
        self.functionEntry.grid(row=2, column=0, columnspan=2)
        self.functionEntry.config(state='disabled')

        # Add all the buttons that allow the user to perform the calculations.
        buttonFrame = Frame(self.frame)

        transposeButton = Button(buttonFrame, text='Transpose', width=10, padx=5, pady=5, command=self.transpose)
        transposeButton.grid(row=0, column=3)

        inverseButton = Button(buttonFrame, text='Inverse', width=10, padx=5, pady=5, command=self.inverse)
        inverseButton.grid(row=1, column=3)

        addButton = Button(buttonFrame, text='+', width=10, padx=5, pady=5, command=self.addition)
        addButton.grid(row=2, column=3)

        multButton = Button(buttonFrame, text='*', width=10, padx=5, pady=5, command=self.multiplication)
        multButton.grid(row=3, column=3)

        eqButton = Button(buttonFrame, text='=', width=10, padx=5, pady=5, command=self.equal)
        eqButton.grid(row=4, column=1)

        buttonOpenBrackets = Button(buttonFrame, text="(", width=10, padx=5, pady=5, command=lambda: self.numberEntered('('))
        buttonOpenBrackets.grid(row=4, column=0)

        buttonCloseBrackets = Button(buttonFrame, text=")", width=10, padx=5, pady=5, command=lambda: self.numberEntered(')'))
        buttonCloseBrackets.grid(row=4, column=2)

        buttonComa = Button(buttonFrame, text=".", width=10, padx=5, pady=5, command=lambda: self.numberEntered('.'))
        buttonComa.grid(row=3, column=0)

        buttonClear = Button(buttonFrame, text="Clear", width=10, padx=5, pady=5, command=self.clearEquation)
        buttonClear.grid(row=3, column=2)

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

        buttonFrame.grid(row=3, column=0)

        self.frame.grid(row=0, column=1, sticky=N + S + E + W)

    def createOperationDictionary(self):
        """
        Create a dictionnary for the operations.
        :return: matrixName: the name of the matrix.
        :return: dictionnary: Dictionary containing all the added command for 'eval' to work.
        """
        a = self.matrixMemory.getMatrices()
        b = []
        for i in a:
            b.append((i[1], i[0]))
        dictionary = dict(b)    # Dict containing the name of the matrices.
        matrixName = dictionary.keys()
        operationsCommand = {'transpose': transpose, 'inverse': inverse}
        # Add the operations to the dictionnaire.
        dictionary.update(operationsCommand)
        return matrixName, dictionary

    def getListOfMatrices(self):
        """
        :return: list of matrix containing in the correct form for display.
        """
        self.allMyMmatrices = self.matrixMemory.getMatrices()
        matrixList = []

        for i in range(len(self.allMyMmatrices)):
            text = self.allMyMmatrices[i][1] + ': (' + str(self.allMyMmatrices[i][0].column_size()) + ' ' \
                   + str(self.allMyMmatrices[i][0].row_size()) + ')'
            matrixList.append((text))
        return matrixList

    def printOnTextArea(self, textToPrint):
        """
        Print to the formulae entry.
        :param textToPrint: The formulae that needs to be entered.
        """
        self.functionEntry.config(state="normal")
        self.functionEntry.delete(0, END)
        self.functionEntry.insert(END, textToPrint)
        self.functionEntry.config(state='disabled')

    def matrixSelected(self, event):
        """
        Save the selected matrix.
        """
        self.text = self.text + self.allMyMmatrices[self.options.index(self.comboBox.get())][1]
        self.operands.append(self.allMyMmatrices[self.options.index(self.comboBox.get())][1])
        self.selectedMatrix = self.allMyMmatrices[self.options.index(self.comboBox.get())][0]
        self.textArea.addMatrixDisplay(self.frame, text=str(self.selectedMatrix))
        self.printOnTextArea(self.text)

######################################################
# ACTION CORRESPONDING TO THE CALCULATOR'S BUTTON
######################################################

    def clearEquation(self):
        self.text = ''
        self.operands = []
        self.printOnTextArea('')

    def numberEntered(self, nmb):
        self.text = self.text + str(nmb)
        self.operands.append(str(nmb))
        self.printOnTextArea(self.text)

    def transpose(self):
        self.text = self.text + 'Transpose('
        self.operands.append('transpose')
        self.operands.append('(')
        self.printOnTextArea(self.text)

    def inverse(self):
        self.text = self.text + 'Inverse('
        self.operands.append('inverse')
        self.operands.append('(')
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
        try:
            answer = eval(self.evaluate(), self.dic)
            self.textArea.printInOutputArea(str(answer))
        except:
            self.textArea.printInOutputArea("Error: The calculation is not correct")

    def evaluate(self):
        """
        This method transform the entered function into an evaluable string.
        :return:
        """
        generalText = ''
        numberID = 0
        i = 0
        while i < len(self.operands):
            if i + 2 < len(self.operands):
                if self.operands[i] in self.matrixNamesList and self.operands[i + 1] == '*' and \
                        self.operands[i + 2] in self.matrixNamesList:
                    name = 'index' + str(numberID)
                    generalText = generalText + name
                    self.dic[name] = np.dot(self.dic.get(self.operands[i]), self.dic.get(self.operands[i + 2]))
                    numberID += 1
                    i += 3
            if i < len(self.operands):
                if self.operands[i] == "+" or self.operands[i] == "*" or self.operands[i] in self.matrixNamesList \
                        or self.operands[i] == "." or self.operands[i].isdigit()  or self.operands[i] == "(" \
                        or self.operands[i] == ")" or self.operands[i] == "transpose" or self.operands[i] == "inverse":
                    generalText = generalText + self.operands[i]
                    i += 1
        return generalText