from tkinter import *
from Menu import MenuTopBar
from Text import TextArea
from Menu import MenuLeftBar

"""
This is the Main file of the programm. This launch the User Interface.
"""

# Create the window on which everything is going to be visible.
root = Tk()
root.title('Ariadne')
# root.geometry("200x200")
# root.geometry("{0}x{1}+0+0".format((root.winfo_screenwidth()),
#                                    (root.winfo_screenheight())))

# Add the text area as well as the line count
textArea = TextArea.MainTextArea()
# textArea.addTextArea(root)
textArea.addOutputArea(root)

# Add the top menu with all the functionalities.
menuBar = MenuTopBar.MenuBar(textArea)
menuBar.addMenuBar(root)

# Add the left menu with the different buttons
leftMenu = MenuLeftBar.MenuWithButton(root, textArea)
leftMenu.addButtonMenu()

# outputTextArea = TextArea.MainTextArea()
# outputTextArea.addOutputArea(root)


status = Label(root, text="Need to put the status here", anchor=E)
status.grid(row=2, column=1, columnspan=2, sticky="EW")

root.mainloop()