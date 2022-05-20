from tkinter import *
import numpy as np
import pandas as pd
from tkinter import filedialog
from pyariadne import *


def getMatrixFromFile():
    """
    This method is used if the user wants to open a .xcel file containing a matrix.
    Read this file and return the matrix contained into the .xcel file.s
    """
    open_file_loc = filedialog.askopenfilename()
    if open_file_loc != '':
        df = pd.read_csv(open_file_loc, header=None, sep=';')
        print('df: ', df)
        myArray = FloatDPApproximationMatrix(df.values.tolist(), dp)
        print(myArray)


        # frame = Frame(self.root)
        #
        # label = Label(frame, text="Name of the matrix:")
        # label.grid(row=0, column=0)
        # e = Entry(frame, width=30, borderwidth=5)
        # e.grid(row=1, column=0)
        #
        # button = Button(frame, text='Get Data', command=lambda: self.matrixMemory.addMatrix(myArray, e.get()))
        # button.grid(row=2, column=0)
        #
        # frame.grid(row=0, column=1)

getMatrixFromFile()