from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog


class MenuBar:
    """
    This class creates the top menu bar.
    """
    def __init__(self, textArea):
        self.textArea = textArea
        self.fontType = "Calibre"

    def openFile(self, event=None):
        """
        Open a file and print it on the text area.
        """
        textIn = self.textArea.getTextWidget()

        open_file_loc = filedialog.askopenfilename()
        if open_file_loc != '':
            open_file = open(open_file_loc, 'r')
            textIn.delete(1.0, END)
            textIn.insert(END, open_file.read())
            self.save_file_id = open_file_loc

    def saveFileAs(self, event=None):
        name = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        text2save = str(self.textArea.getTextWidget().get(0.0, END))
        name.write(text2save)
        name = str(name)[(str(name).find("name='") + 6):str(name).find("'", (str(name).find("name='") + 6))]
        self.save_file_id = name

    def save_file(self, event=None):
        if self.save_file_id == "":
            self.save_as_file()
        else:
            with open(self.save_file_id, 'w') as f:
                f.write(self.textArea.getTextWidget().get(0.0, END))

    def new_file(self, event=None):
        # TODO add a verification saving window.
        self.textArea.getTextWidget().delete(1.0, END)
        save_file_id = ''

    def font_size(self):
        """Adjust Font Size"""
        newFontSize = simpledialog.askstring(
            "Font", "Enter font size", parent=self.root)
        self.textArea.getTextWidget().config(font=str(self.fontType + ' ' + newFontSize))
        self.textArea.getTextWidget().update

    def addMenuBar(self, root):
        """
        Create and add the element on the screen such that the top bar is visible.
        :param root: The window on which to display the top bar.
        :return:
        """
        self.root = root
        # Create a menu
        my_menu = Menu(root)
        # Add the file menu
        fileMenu = Menu(my_menu, tearoff=False)
        my_menu.add_cascade(label='file', menu=fileMenu)
        fileMenu.add_command(label='New', command=self.new_file, accelerator="Ctrl+n")
        fileMenu.add_command(label='Open', command=self.openFile, accelerator="Ctrl+o")
        fileMenu.add_command(label='Save', command=self.save_file, accelerator="Ctrl+s")
        fileMenu.add_command(label='Save as', command=self.saveFileAs, accelerator="Ctrl++")

        # https://gist.github.com/angeloped/91fb1bb00f1d9e0cd7a55307a801995f
        #the_menu.entryconfigure("Cut", command=lambda: e_widget.event_generate("<<Cut>>"))
        #the_menu.entryconfigure("Copy", command=lambda: e_widget.event_generate("<<Copy>>"))
        #the_menu.entryconfigure("Paste", command=lambda: e_widget.event_generate("<<Paste>>"))
        # the_menu.entryconfigure("Select all", command=lambda: e_widget.select_range(0, 'end'))

        fileMenu.add_separator()
        fileMenu.add_command(label='Close')

        viewMenu = Menu(my_menu, tearoff=False)
        my_menu.add_cascade(label='view', menu=viewMenu)
        viewMenu.add_command(label='Font Size', command=self.font_size)

        fileMenu.bind_all("<Control-o>", self.openFile)
        fileMenu.bind_all("<Control-n>", self.new_file)
        fileMenu.bind_all("<Control-a>", self.saveFileAs)
        fileMenu.bind_all("<Control-s>", self.save_file)
        root.config(menu=my_menu)
        # TODO add a Run button ??