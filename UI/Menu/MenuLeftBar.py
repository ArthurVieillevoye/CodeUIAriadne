from tkinter import *
from UI.Menu.MatrixHandeler import MatrixCreation
from UI.Menu.MatrixHandeler import MatrixSelection
from UI.Menu.MatrixHandeler import MatrixOperation
from UI.Menu.MatrixHandeler import MatrixEigen


class MenuWithButton:
    """
    This class contains all the 'visible' element on the left bar.
    It contains the description of the buttons and the link with their corresponding command.
    """
    def __init__(self, root, textArea):
        self.root = root
        self.textArea = textArea
        self.matrixMemory = MatrixSelection.Matrices(self.root, self.textArea)

    def addButtonMenu(self):
        """
        Add all the buttons on the left side of the main window and link them to the corresponding command.
        """
        # Create the frame
        frame = Frame(self.root)

        # Add the different buttons
        buttonNewMatrix = Button(frame, text="New Matrix", padx=5, pady=5, width=16, command=self.newMatrixButtonAction)
        buttonNewMatrix.grid(row=0, column=0, padx=5, pady=5)

        buttonMyMatrix = Button(frame, text="My Matrices", padx=5, pady=5, width=10, command=self.myMatricesButtonActive)
        buttonMyMatrix.grid(row=1, column=0, sticky="new", padx=5, pady=5)

        buttonAddMatrix = Button(frame, text="Matrix Operation", padx=5, pady=5, width=10, command=self.matrixOperationButtonActive)
        buttonAddMatrix.grid(row=2, column=0, sticky="new", padx=5, pady=5)

        buttonAddMatrix = Button(frame, text="Matrix Eigen", padx=5, pady=5, width=10, command=self.matrixEigenButtonActive)
        buttonAddMatrix.grid(row=3, column=0, sticky="new", padx=5, pady=5)
        frame.grid(row=0, column=0, sticky="new", padx=5, pady=5)

    def matrixEigenButtonActive(self):
        """
        Lead to the matrix eigen computation section.
        This section allows the user to compute and render the eigenvalues/eigenvectors of its matrices.
        """
        # Clear the text output Area
        self.textArea.deleteAll()

        # Create the corresponding object and display it.
        eigenWindow = MatrixEigen.MatrixEigen(self.root, self.textArea, self.matrixMemory)
        eigenWindow.addEigenWindow()

    def matrixOperationButtonActive(self):
        """
        Lead to the matrix operation section.
        That section allows the user to do some basic matrix operations with its matrices.
        """
        # Clear the text output Area
        self.textArea.deleteAll()

        # Create the corresponding object and display it.
        operationWindow = MatrixOperation.MatrixMult(self.root, self.textArea, self.matrixMemory)
        operationWindow.addMultiplicationWindow()

    def myMatricesButtonActive(self):
        """
        Leads to the matrix memory section.
        That section allows the user to see, modify, copy and delete the matrix he created.
        """
        # Clear the text output Area
        self.textArea.deleteAll()

        # Display the matrix memory frame.
        self.root.grid_slaves()[0].grid_forget()
        self.matrixMemory.seeMatrices()

    def newMatrixButtonAction(self):
        """
        Leads to the matrix creation section.
        That sectioallows the user to properly entered its matrix.
        """
        # Clear the text output Area
        self.textArea.deleteAll()

        # Create the corresponding object and display it.
        m = MatrixCreation.MatrixCreationWindow(self.root, textArea=self.textArea,
                                                matrixMemory=self.matrixMemory)
        m.addMatrixCreationOptions()