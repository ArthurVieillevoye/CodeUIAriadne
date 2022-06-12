from tkinter import *
from tkinter.ttk import Combobox
from EigenComputation import Householder
from EigenComputation import IntervalNewtonMethod
from EigenComputation import EigenVecotrs
from pyariadne import *


class MatrixEigen:
    """
    This class is responsible for all of the matrix eigenComputaion graphical user interface.
    """
    def __init__(self, root, textArea, matrixMemory):
        self.root = root
        self.textArea = textArea
        self.matrixMemory = matrixMemory

    def addEigenWindow(self):
        """
        Display the frame that allows the user to choose if he wants all of one eigen.
        """
        self.frame = Frame(self.root)

        label1 = Label(self.frame, text="Select symmetric matrix:")
        label1.grid(row=0, column=0)

        self.options = self.getListOfMatrices()
        # Add the comboBox containing all the matrices.
        self.comboBox = Combobox(self.frame, value=self.options)
        self.comboBox.bind("<<ComboboxSelected>>", self.matrixSelected)
        self.comboBox.grid(row=1, column=0)

        buttonAllEigen = Button(self.frame, text="All eigen", padx=5, pady=5, width=8,
                                command=self.allEigenButtonActive)
        buttonAllEigen.grid(row=2, column=0)
        buttonAllEigen = Button(self.frame, text="One Eigen", padx=5, pady=5, width=8, command=self.oneEigenButtonActive)
        buttonAllEigen.grid(row=3, column=0, sticky=N)

        self.frame.grid(row=0, column=1, sticky=N + S + E + W)

    def getListOfMatrices(self):
        """
        :return: the matrix into a nicer way to display them.
        """
        self.allMyMmatrices = self.matrixMemory.getMatrices()
        matrixList = []

        for i in range(len(self.allMyMmatrices)):
            text = self.allMyMmatrices[i][1] + ': (' + str(self.allMyMmatrices[i][0].row_size()) + " " + \
                   str(self.allMyMmatrices[i][0].column_size()) + ")"
            matrixList.append((text))
        return matrixList

    def matrixSelected(self, event):
        """
        Save the selected matrix for later use.
        """
        self.clearFrame()

        self.selectedMatrix = self.allMyMmatrices[self.options.index(self.comboBox.get())][0]
        self.textArea.addMatrixDisplay(self.frame, text=str(self.selectedMatrix))

    def allEigenButtonActive(self):
        """
        Compute and display all of the eigenValues and eigenVectors.
        """
        try:
            eigenValues, eigenVectors = Householder.findEigenAriadne(self.selectedMatrix)

            self.eigenValuesList = []
            self.eigenVectorList = []
            for i in range(len(eigenValues)):
                # Compute an interval for all of the eigenValues and eigenvectors.
                eigenVect, eigenVal = IntervalNewtonMethod.intervalNewtonMethods(Householder.getColumn(i, eigenVectors),
                                                                                 eigenValues[i], self.selectedMatrix)
                self.eigenValuesList.append(eigenVal)
                self.eigenVectorList.append(eigenVect)
            self.displayFoundEigen()
        except:
            # Throw an error if no matrix has been selected.
            self.textArea.printInOutputArea("Error: No matrix selected")

    def oneEigenButtonActive(self):
        """
        Gives the eigen options. (gives the user the option to giva an estimate of the wished eigen.
        """
        try:
            self.selectedMatrix.row_size()

            # Clean the frame.
            self.clearFrame()

            # Add the labels and the entries to allow the user to enter its estimate.
            label = Label(self.frame, text = "eigenvalue estimate (optional): ")
            label.grid(row=2, column=1)
            self.entry1 = Entry(self.frame, width=30)
            self.entry1.grid(row=3, column=1)
            label = Label(self.frame, text="Eigenvector estimate (optional): ")
            label.grid(row=4, column=1)
            self.entry2 = Entry(self.frame, width=30)
            self.entry2.grid(row=5, column=1)

            computerEigenButton = Button(self.frame, text="get Eigen", padx=5, pady=5, command= self.getEigenComputed)
            computerEigenButton.grid(row=6, column=1)
        except:
            self.textArea.printInOutputArea("Error: No matrix selected")


    def getEigenComputed(self):
        """
        Compute the eigenValues and eigenvectors.
        :return:
        """
        if self.entry1.get() !='' and self.entry2.get() !='':
            # Compute the closest eigen to the estimate.
            eigenValEstimate = FloatDPApproximation(eval(self.entry1.get()), dp)
            eigenVectEstimate = self.decodeEnteredMatrix(self.entry2.get())
            eigenVect, eigenVal = IntervalNewtonMethod.intervalNewtonMethods(eigenVectEstimate, eigenValEstimate, self.selectedMatrix)
            self.eigenVectorList = [eigenVect]
            self.eigenValuesList = [eigenVal]
            self.displayFoundEigen()

        else:
            # Compute any eigen if the user has not entered any approximation.
            eigenValEstimate, eigenVectEstimate = EigenVecotrs.power_methods(self.selectedMatrix)
            eigenVect, eigenVal = IntervalNewtonMethod.intervalNewtonMethods(eigenVectEstimate, eigenValEstimate, self.selectedMatrix)
            self.eigenVectorList = [eigenVect]
            self.eigenValuesList = [eigenVal]
            self.displayFoundEigen()

    def decodeEnteredMatrix(self, matrix):
        """
        Verify that the estimations has been entered properly.
        :param matrix: The estimate of the eigen.
        :return: the estimated eigenvector into Ariadne form.
        """
        try:
            return FloatDPApproximationVector(eval(matrix), dp)
        except:
            self.textArea.printInOutputArea('You did not enter the eigenvector approximation in a correct form')

    def displayFoundEigen(self):
        """
        Display the found eigenvectors and eigenvalues.
        Also add different options to the user considering the eigen.
        """
        # Clean the frame.
        self.clearFrame()

        # Add to the frame the found estimate and the different user choices (buttons).
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

    def gtc(self, i, midPoint):
        """
        Allow the user to copy the selected estimate. (put the estimate into the clipboard).
        :param i: The index of the selected matrix.
        :param midPoint: boolean that indicates if the user wants the midpoint of the bound or not
        """
        self.root.clipboard_clear()
        if midPoint:
            selectedEigen = (cast_exact(self.eigenValuesList[i]), cast_exact(self.eigenVectorList[i]))
        else:
            selectedEigen = (self.eigenValuesList[i], self.eigenVectorList[i])

        self.root.clipboard_append(selectedEigen)

    def printEstimate(self, i, midPoint):
        """
        Print the selected matrix to the output text area.
        :param i: The index of the selected matrix.
        :param midPoint: boolean that indicates if the user wants the midpoint of the bound or not
        """
        if midPoint:
            sentence = repr(cast_exact(self.eigenValuesList[i])) + " : " + repr(cast_exact(self.eigenVectorList[i])) + '\n'
        else:
            sentence = repr(self.eigenValuesList[i]) + " : " + repr(self.eigenVectorList[i]) + '\n'
        self.textArea.printInOutputArea(sentence)

    def clearFrame(self):
        """
        Clears the frame.
        """
        for label in self.frame.grid_slaves():
            if int(label.grid_info()["column"]) > 0:
                label.destroy()