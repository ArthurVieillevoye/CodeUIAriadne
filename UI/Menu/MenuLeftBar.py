from tkinter import *
from UI.Menu.MatrixHandeler import MatrixCreation
from UI.Menu.MatrixHandeler import MatrixSelection
from UI.Menu.MatrixHandeler import MatrixOperation
from UI.Menu.MatrixHandeler import MatrixEigen


class MenuWithButton:
    """
    This class contains all the 'visible' element visible into the left bar.
    It contains the description of the buttons and the link with their corresponding command.
    """
    def __init__(self, root, textArea):
        self.root = root
        self.textArea = textArea
        self.matrixMemory = MatrixSelection.Matrices(self.root, self.textArea)

    def matrixOperationButtonActive(self):
        self.textArea.deleteAll()
        operationWindow = MatrixOperation.MatrixMult(self.root, self.textArea, self.matrixMemory)
        self.root.grid_slaves()[0].grid_forget()
        operationWindow.addMultiplicationWindow()

    def matrixEigenButtonActive(self):
        self.textArea.deleteAll()
        eigenWindow = MatrixEigen.MatrixEigen(self.root, self.textArea, self.matrixMemory)
        self.root.grid_slaves()[0].grid_forget()
        eigenWindow.addEigenWindow()

    def myMatricesButtonActive(self):
        self.textArea.deleteAll()
        self.root.grid_slaves()[0].grid_forget()
        self.matrixMemory.seeMatrices()

    # def runButtonActive(self):
    #     path ="C:/Users/Arthur Vieillevoye/Documents/university/Current Class/Thesis/Code/UI/RunTest.py"

        # nPath = path.replace(' ', '\\ ')
        # exec(open(path).read())

    def bMatrixFromFile(self):
        """
        Call the matrixCreation object.
        Allow the user choose an excel file containing a matrix.
        """
        m = MatrixCreation.MatrixCreationWindow(self.newMatrixFrame, textArea=self.textArea, matrixMemory=self.matrixMemory)
        m.getMatrixFromFile()

    # def addMatrixWindow(self):
    #     """
    #     Call the matrixCreation object.
    #     Allow the user to enter himself the matrix into a intuitive way.
    #     """
    #     m = MatrixCreation.MatrixCreationWindow(self.root, int(self.e1.get()), int(self.e2.get()), matrixMemory=self.matrixMemory)
    #     m.addMatrixWindow()

    def bMatrixEnter(self):
        """
        This methods creates the window on which the user can enter the size of the matrix he wants to enter.
        """
        m = MatrixCreation.MatrixCreationWindow(self.newMatrixFrame, textArea=self.textArea, matrixMemory=self.matrixMemory)
        m.addMatrixWindow()

    def bMatrixWrite(self):
        # self.buttonEnter.grid_remove()
        # self.buttonWrite.grid_remove()
        # self.buttonMatrixFromFile.grid_remove()
        m = MatrixCreation.MatrixCreationWindow(self.newMatrixFrame, textArea=self.textArea, matrixMemory=self.matrixMemory)
        m.addMatrixTextWindow()


    def newMatrixButtonAction(self):
        """
        Create the window that allows the user to choose how he wants to enter his/her matrix.
        """
        self.root.grid_slaves()[0].grid_forget()
        self.textArea.deleteAll()

        self.newMatrixFrame = Frame(self.root)
        # self.newWindow.geometry("200x200")
        self.buttonEnter = Button(self.newMatrixFrame, text="Enter Matrix", padx=5, pady=5,
                                  command=self.bMatrixEnter)
        self.buttonEnter.grid(row=0, column=0, sticky="new")

        self.buttonWrite = Button(self.newMatrixFrame, text="Write Matrix", padx=5, pady=5,
                                  command=self.bMatrixWrite)
        self.buttonWrite.grid(row=1, column=0, sticky="new")

        self.buttonMatrixFromFile = Button(self.newMatrixFrame, text="Upload Matrix", padx=5, pady=5,
                                  command=self.bMatrixFromFile)
        self.buttonMatrixFromFile.grid(row=2, column=0, sticky="new")

        self.newMatrixFrame.grid(row=0, column=1, sticky=N + S + E + W)

    def addButtonMenu(self):
        """
        Add all the neccessary buttons on the left side of the main window.
        """
        frame = Frame(self.root)
        buttonNewMatrix = Button(frame, text="New Matrix", padx=5, pady=5, width=16, command=self.newMatrixButtonAction)
        buttonNewMatrix.grid(row=0, column=0, padx=5, pady=5)

        buttonMyMatrix = Button(frame, text="My Matrices", padx=5, pady=5, width=10, command=self.myMatricesButtonActive)
        buttonMyMatrix.grid(row=1, column=0, sticky="new", padx=5, pady=5)

        # buttonRun = Button(frame, text="Run", padx=25, pady=5, width=10, command=self.runButtonActive)
        # buttonRun.grid(row=2, column=0, sticky="new", padx=5, pady=5)

        buttonAddMatrix = Button(frame, text="Matrix Operation", padx=5, pady=5, width=10, command=self.matrixOperationButtonActive)
        buttonAddMatrix.grid(row=2, column=0, sticky="new", padx=5, pady=5)

        buttonAddMatrix = Button(frame, text="Matrix Eigen", padx=5, pady=5, width=10, command=self.matrixEigenButtonActive)
        buttonAddMatrix.grid(row=3, column=0, sticky="new", padx=5, pady=5)
        frame.grid(row=0, column=0, sticky="new", padx=5, pady=5)
