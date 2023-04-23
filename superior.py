import inferior
import tkinter as tk

# root.winfo_screenwidth()
# root.winfo_screenheight()
# widget.place(anchor="nw", x=0, y=0, width=0, height=0)

units = [int(x.replace('U>', '')) for x in inferior.units_indexes.keys()]

root = tk.Tk()
root.title('APHG Progress Checks Practice')
root.geometry('1000x800')

start_page = tk.Frame(root)
start_page.pack()

quiz_page = tk.Frame(root)

tk.Label(start_page, text='AP Progress Checks', font=('Arial', 44)).pack()

def create_choose_frame():
    global chosen, choose_frame; chosen = []
    choose_frame = tk.Canvas(start_page)
    choose_frame.pack()
    tk.Button(choose_frame, text='Begin Practice', font=('Arial', 20), command=begin).pack(pady=10)
    [create_unit_button(unit) for unit in units]

def create_unit_button(unit):
    global chosen; chosen.append(tk.IntVar())
    tk.Checkbutton(choose_frame, text=f'Unit {unit}', font=('Arial', 15), variable=chosen[-1], onvalue=1, offvalue=0).pack(pady=5)

def get_questions():
    global questions; questions = []
    for i, unit in enumerate(chosen, start=1):
        if unit.get() == 1:
            unit_lines = inferior.get_unit_lines(i)
            questions += inferior.get_questions_lines(unit_lines)

##########################################

def begin():
    get_questions()
    start_page.pack_forget()

create_choose_frame()



#####################

root.mainloop()