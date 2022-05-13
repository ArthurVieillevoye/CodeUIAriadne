from tkinter import *


def button_clicked(number):
    current = e.get()
    e.delete(0, END)
    e.insert(0, str(current) + str(number))


def button_clear():
    e.delete(0, END)


def button_add():
    number = e.get()
    global num
    global operation
    operation = "Addition"
    num = int(number)
    e.delete(0, END)


def button_sub():
    number = e.get()
    global num
    global operation
    operation = "Substraction"
    num = int(number)
    e.delete(0, END)


def button_mult():
    number = e.get()
    global num
    global operation
    operation = "Multiplication"
    num = int(number)
    e.delete(0, END)


def button_div():
    number = e.get()
    global num
    global operation
    operation = "Division"
    num = int(number)
    e.delete(0, END)


def button_equal():
    secNum = e.get()
    e.delete(0, END)

    if operation == "Addition":
        e.insert(0, num + int(secNum))
    elif operation == "Substraction":
        e.insert(0, num - int(secNum))
    elif operation == "Multiplication":
        e.insert(0, num * int(secNum))
    elif operation == "Division":
        e.insert(0, num / int(secNum))
    else:
        e.insert(0, "error")


root = Tk()
root.title("Try Calculator")

e = Entry(root, width=60, borderwidth=5)
e.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

button0 = Button(root, text="0", padx=40, pady=20, command=lambda: button_clicked(0))
button1 = Button(root, text="1", padx=40, pady=20, command=lambda: button_clicked(1))
button2 = Button(root, text="2", padx=40, pady=20, command=lambda: button_clicked(2))
button3 = Button(root, text="3", padx=40, pady=20, command=lambda: button_clicked(3))
button4 = Button(root, text="4", padx=40, pady=20, command=lambda: button_clicked(4))
button5 = Button(root, text="5", padx=40, pady=20, command=lambda: button_clicked(5))
button6 = Button(root, text="6", padx=40, pady=20, command=lambda: button_clicked(6))
button7 = Button(root, text="7", padx=40, pady=20, command=lambda: button_clicked(7))
button8 = Button(root, text="8", padx=40, pady=20, command=lambda: button_clicked(8))
button9 = Button(root, text="9", padx=40, pady=20, command=lambda: button_clicked(9))

buttonAdd = Button(root, text="+", padx=39, pady=20, command=button_add)
buttonDivide = Button(root, text="/", padx=40, pady=20, command=button_div)
buttonMulti = Button(root, text="*", padx=40, pady=20, command=button_mult)
buttonSub = Button(root, text="-", padx=40, pady=20, command=button_sub)
buttonEqual = Button(root, text="=", padx=40, pady=20, command=button_equal)
buttonClear = Button(root, text="clear", padx=31, pady=20, command=button_clear)

button0.grid(row=4, column=1)

button1.grid(row=3, column=0)
button2.grid(row=3, column=1)
button3.grid(row=3, column=2)

button4.grid(row=2, column=0)
button5.grid(row=2, column=1)
button6.grid(row=2, column=2)

button7.grid(row=1, column=0)
button8.grid(row=1, column=1)
button9.grid(row=1, column=2)

buttonAdd.grid(row=1, column=3)
buttonSub.grid(row=2, column=3)
buttonMulti.grid(row=3, column=3)
buttonDivide.grid(row=4, column=3)
buttonClear.grid(row=4, column=0)
buttonEqual.grid(row=4, column=2)

root.mainloop()
