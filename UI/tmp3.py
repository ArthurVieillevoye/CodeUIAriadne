import numpy as np
import tkinter as tk  # PEP8: `import *` is not preferred


# --- functions ---

def get_data():
    for r, row in enumerate(all_entries):
        for c, entry in enumerate(row):
            text = entry.get()
            demand[r, c] = float(text)

    print(demand)


# --- main ---

rows = 19
cols = 5

demand = np.zeros((rows, cols))

window = tk.Tk()

for c in range(cols):
    l = tk.Label(window, text=str(c))
    l.grid(row=0, column=c + 1)

all_entries = []
for r in range(rows):
    entries_row = []
    l = tk.Label(window, text=str(r + 1))
    l.grid(row=r + 1, column=0)
    for c in range(cols):
        e = tk.Entry(window, width=5)  # 5 chars
        e.insert('end', 0)
        e.grid(row=r + 1, column=c + 1)
        entries_row.append(e)
    all_entries.append(entries_row)

b = tk.Button(window, text='GET DATA', command=get_data)
b.grid(row=rows + 1, column=0, columnspan=cols)

window.mainloop()