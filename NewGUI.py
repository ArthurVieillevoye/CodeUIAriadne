from tkinter import *
from UI.Text import TextArea
from UI.Menu import MenuLeftBar

"""
This is the Main file of the programm. This launch the User Interface.
"""

if __name__ == "__main__":
    # Create the window on which everything is going to be visible.
    root = Tk()
    root.title('Ariadne')

    # Add the text area as well as the line count
    textArea = TextArea.MainTextArea()
    # textArea.addTextArea(root)
    textArea.addOutputArea(root)

    # Add the left menu with the different buttons
    leftMenu = MenuLeftBar.MenuWithButton(root, textArea)
    leftMenu.addButtonMenu()

    status = Label(root, text="", anchor=E)
    status.grid(row=2, column=1, columnspan=2, sticky="EW")

    root.mainloop()