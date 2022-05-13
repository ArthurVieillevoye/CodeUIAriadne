from tkinter import *
from UI.Menu.MatrixHandeler import MatrixCreation
from UI.Menu.MatrixHandeler import MatrixSelection
from UI.Menu.MatrixHandeler import MatrixOperation


class MenuWithButton:
    """
    This class contains all the 'visible' element visible into the left bar.
    It contains the description of the buttons and the link with their corresponding command.
    """
    def __init__(self, root, textArea):
        self.root = root
        self.textArea = textArea
        self.matrixMemory = MatrixSelection.Matrices(self.root, self.textArea)

    def addButtonActive(self):
        multButton = MatrixOperation.MatrixMult(self.root, self.matrixMemory, self.textArea, self.matrixMemory)
        multButton.addMultiplicationWindow()


    def myMatricesButtonActive(self):
        self.matrixMemory.seeMatrices()

    def runButtonActive(self):
        path ="C:/Users/Arthur Vieillevoye/Documents/university/Current Class/Thesis/Code/UI/RunTest.py"

        # nPath = path.replace(' ', '\\ ')
        exec(open(path).read())

    def bMatrixFromFile(self):
        """
        Call the matrixCreation object.
        Allow the user choose an excel file containing a matrix.
        """
        m = MatrixCreation.MatrixCreationWindow(self.root, matrixMemory=self.matrixMemory)
        m.getMatrixFromFile()

    def addMatrixWindow(self):
        """
        Call the matrixCreation object.
        Allow the user to enter himself the matrix into a intuitive way.
        """
        m = MatrixCreation.MatrixCreationWindow(self.root, int(self.e1.get()), int(self.e2.get()), matrixMemory=self.matrixMemory)
        m.addMatrixWindow()

    def bMatrixWrite(self):
        """
        This methods creates the window on which the user can enter the size of the matrix he wants to enter.
        """
        m = MatrixCreation.MatrixCreationWindow(self.root, matrixMemory=self.matrixMemory)
        m.addMatrixWindow()


    def newMatrixButtonAction(self):
        """
        Create the window that allows the user to choose how he wants to enter his/her matrix.
        """
        newWindow = Toplevel(master=self.root)
        newWindow.title("New Matrix")
        # self.newWindow.geometry("200x200")
        self.buttonWrite = Button(newWindow, text="Write Matrix", padx=5, pady=5,
                                  command=self.bMatrixWrite)
        self.buttonWrite.grid(row=0, column=0)

        self.buttonMatrixFromFile = Button(newWindow, text="Upload Matrix", padx=5, pady=5,
                                  command=self.bMatrixFromFile)
        self.buttonMatrixFromFile.grid(row=1, column=0)

    def addButtonMenu(self):
        """
        Add all the neccessary buttons on the left side of the main window.
        """
        frame = Frame(self.root)
        buttonNewMatrix = Button(frame, text="New Matrix", padx=5, pady=5, width=16, command=self.newMatrixButtonAction)
        buttonNewMatrix.grid(row=0, column=0, padx=5, pady=5)

        buttonMyMatrix = Button(frame, text="My Matrices", padx=5, pady=5, width=10, command=self.myMatricesButtonActive)
        buttonMyMatrix.grid(row=1, column=0, sticky="new", padx=5, pady=5)

        buttonRun = Button(frame, text="Run", padx=25, pady=5, width=10, command=self.runButtonActive)
        buttonRun.grid(row=2, column=0, sticky="new", padx=5, pady=5)

        buttonAddMatrix = Button(frame, text="Matrix Operation", padx=5, pady=5, width=10, command=self.addButtonActive)
        buttonAddMatrix.grid(row=3, column=0, sticky="new", padx=5, pady=5)
        frame.grid(row=0, column=0, sticky="new", padx=5, pady=5)
