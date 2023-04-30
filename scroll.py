import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title('Hello World')
root.geometry('500x400')

canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

second_frame = tk.Frame(canvas)

canvas.create_window((0, 0), window=second_frame, anchor=tk.NW)

def add_button():
    tk.Button(second_frame, text=f'asdf', command=add_button).pack()
    canvas.event_generate('<Configure>')

add_button()

root.mainloop()