from tkinter import *


# TODO move the line number with the finger moves

class MainTextArea:
    """
    This class generates tha main textArea
    The main textArea is where the user will enter its text.
    It is also responsible for all the options relative to the textArea.
    """

    def addTextArea(self, root):
        """
        Create and add the main text area to the root window.
        :param root: The window on which the textArea has to appear.
        """

        def multiple_yview(*args):
            l.changeView(*args)
            self.text.yview(*args)

        # Generating the frame
        frame = Frame(root)
        # frame.pack(pady=5)

        # ScrollBar for the textBox
        scroll = Scrollbar(frame)
        scroll.pack(side=RIGHT, fill=Y)
        hScroll = Scrollbar(frame, orient="horizontal")
        hScroll.pack(side=BOTTOM, fill=X)

        # Create the text area
        self.text = Text(frame, undo=True, width=150, height=30, wrap=NONE,
                         yscrollcommand=scroll.set, xscrollcommand=hScroll.set)

        # Add the line numbers:
        l = LineNumber(frame)
        l.addLineNumber()

        # Bind any line adding to the update of the line number.
        root.bind_all('<Return>', lambda event: l.redraw(self.text))
        root.bind_all('<BackSpace>', lambda event: l.redraw(self.text))
        root.bind_all('<Key>', lambda event: l.redraw(self.text))
        root.bind_all('<Button-4>', lambda event: l.redraw(self.text))
        root.bind_all('<Button-5>', lambda event: l.redraw(self.text))
        root.bind_all('<Configure>', lambda event: l.redraw(self.text))
        root.bind_all('<Motion>', lambda event: l.redraw(self.text))

        self.text.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.config(command=multiple_yview)
        hScroll.config(command=self.text.xview)
        frame.grid(row=0, column=1, sticky=N+S+E+W)


    def addOutputArea(self, root):
        """
        Create and add the main text area to the root window.
        :param root: The window on which the textArea has to appear.
        """
        # Generating the frame
        frame = Frame(root)
        # frame.pack(pady=5)

        # ScrollBar for the textBox
        vScroll = Scrollbar(frame)
        vScroll.pack(side=RIGHT, fill=Y)

        hScroll = Scrollbar(frame, orient="horizontal")
        hScroll.pack(side=BOTTOM, fill=X)
        # Create the text area
        self.textOutput = Text(frame, undo=True, width=150, height=10, state=DISABLED,
                         yscrollcommand=vScroll.set, xscrollcommand=hScroll.set)
        # TODO: add a horizontal scroll bar.

        self.textOutput.pack(side=LEFT, fill=BOTH, expand=True)
        vScroll.config(command=self.textOutput.yview)
        hScroll.config(command=self.textOutput.xview)
        frame.grid(row=1, column=1, sticky=N+S+E+W)

    def printInOutputArea(self, textToPrint):
        self.textOutput.config(state="normal")
        self.textOutput.insert(END, textToPrint)
        self.textOutput.config(state='disabled')

    def getTextWidget(self):
        """
        Getter method.
        :return: the main text area.
        """
        return self.text


class LineNumber:
    """
    This class defines the lineCount element next to the textArea.
    """
    def __init__(self, root):
        self.lineNumber = Canvas(root, width="30")

    def addLineNumber(self):
        # Add the element containing the number of line to the window.
        self.lineNumber.pack(side=LEFT, fill=Y)

    def redraw(self, textWidgit, event=NONE):
        """
        Update the number of line element in case of modification of the size of the file.
        """
        count = textWidgit.get('1.0', END)
        self.lineNumber.delete("all")
        objectIds = []
        si = textWidgit.index("@0,0")
        while True:
            dline = textWidgit.dlineinfo(si)
            if dline is None:
                break
            y = dline[1]
            liNum = str(si).split(".")[0]
            self.lineNumber.create_text(
                2, y, anchor="nw", text=liNum, )
            si = textWidgit.index(f"{si}+1line")

    def changeView(self, *args):
        self.lineNumber.yview(*args)