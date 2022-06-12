from tkinter import *

class MainTextArea:
    """
    This class generates the textAreas
    It is responsible for all the options relative to the textArea and for the matrix display when they are selected.
    """

    def addMatrixDisplay(self, root, text= ''):
        """
        Create and add the matrix display text area. This method will show to the user the matrix that he selected.
        :param root: The window on which the textArea has to appear.
        :param text: The text that need to be displayed on the textArea.
        """
        # Generating the frame
        frame = Frame(root)
        # frame.pack(pady=5)

        # ScrollBar for the textBox
        scroll = Scrollbar(frame)
        scroll.pack(side=RIGHT, fill=Y)
        hScroll = Scrollbar(frame, orient="horizontal")
        hScroll.pack(side=BOTTOM, fill=X)

        # Create the text area
        self.textArea = Text(frame, undo=True, width=45, height=9, wrap=NONE,
                         yscrollcommand=scroll.set, xscrollcommand=hScroll.set)

        # Set and add the text to the textArea.
        text = text.replace(";", ";\n")
        self.textArea.config(state="normal")
        self.textArea.delete("1.0", END)
        self.textArea.insert(END, text)
        self.textArea.config(state='disabled')

        self.textArea.pack(side=LEFT, fill=BOTH, expand=True)
        hScroll.config(command=self.textArea.xview)
        frame.grid(row=0, column=2, rowspan=20, sticky=N+E+W)


    def addOutputArea(self, root):
        """
        Create and add the output text area to the root window.
        All the information returned to the user will be printed on this textArea (error, print, etc.).
        :param root: The frame on which the textArea has to appear.
        """
        # Generating the frame
        frame = Frame(root)

        # ScrollBar for the textBox
        vScroll = Scrollbar(frame)
        vScroll.pack(side=RIGHT, fill=Y)

        hScroll = Scrollbar(frame, orient="horizontal")
        hScroll.pack(side=BOTTOM, fill=X)

        # Create the text area
        self.textOutput = Text(frame, undo=True, width=100, height=10, state=DISABLED,
                         yscrollcommand=vScroll.set, xscrollcommand=hScroll.set)

        # Add the textArea to the frame.
        self.textOutput.pack(side=LEFT, fill=BOTH, expand=True)
        vScroll.config(command=self.textOutput.yview)
        hScroll.config(command=self.textOutput.xview)
        frame.grid(row=1, column=1, sticky=N+S+E+W)

    def printInOutputArea(self, textToPrint):
        """
        Printxt on the output textArea
        :param textToPrint: The text that needs to be printed.
        """
        textToPrint = textToPrint + "\n"
        self.textOutput.config(state="normal")
        self.textOutput.insert(END, textToPrint)
        self.textOutput.see('end')
        self.textOutput.config(state='disabled')

    def deleteAll(self):
        """
        Clear the output textArea. This method is called when the user goes to another section of the GUI.
        """
        self.textOutput.config(state="normal")
        self.textOutput.delete("1.0", END)
        self.textOutput.config(state='disabled')