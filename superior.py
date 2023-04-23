import inferior
import tkinter as tk
import random
from PIL import ImageTk, Image
import os

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

def get_questions_lines():
    global questions_lines, images; questions_lines = []
    for i, unit in enumerate(chosen, start=1):
        if unit.get() == 1:
            unit_lines = inferior.get_unit_lines(i)
            questions_lines += inferior.get_questions_lines(unit_lines)
    #random.shuffle(questions_lines)

##########################################

def get_image(name, unit, height=300):
    image = Image.open(f'images/{unit}/{name}')
    og_image_w, og_image_h = image.size
    return ImageTk.PhotoImage(image.resize((int(og_image_w/og_image_h*height), int(height))))

def create_images():
    global images; images = {}
    image_folders = os.listdir(path='images')
    for folder in image_folders:
        folder_images = os.listdir(path=f'images/{folder}')
        for image in folder_images:
            images[image] = get_image(image, folder)

def begin():
    global question_num; question_num = 1
    get_questions_lines()
    start_page.pack_forget()
    quiz_page.pack()
    update_question(question_num)
##

def submit_question():
    global question_num; question_num += 1
    if question_num <= len(questions_lines):
        update_question(question_num)

def set_choice(index, all_choices):
    choice_parts = all_choices[index]
    choices_vars[index].set(choice_parts[0])
    choices_explanations[index].set(choice_parts[1] if len(choice_parts) == 2 else '')
    print([x.get() for x in choices_vars])

def update_question(question_num):
    question_parts = inferior.get_question(questions_lines[question_num-1])

    image_parts = question_parts[5]
    if len(image_parts) != 0:
        image_label.pack()
        image_label.config(image=images[image_parts[0]])
        if len(image_parts) == 2: image_text_label.config(text=image_parts[1])
    elif image_label.winfo_ismapped():
        image_label.pack_forget()

    question_label.config(text=question_parts[0])

    all_choices = [question_parts[1]] + question_parts[2]; random.shuffle(all_choices)

    for i in range(5): set_choice(i, all_choices)

##
image_text_var = tk.StringVar()

chosen_var = tk.IntVar()

choices_vars = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
choices_explanations = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
##

submit_button = tk.Button(quiz_page, text='Submit', command=submit_question)
submit_button.pack()

question_label = tk.Label(quiz_page)
question_label.pack()

image_canvas = tk.Canvas(quiz_page)
image_canvas.pack()
image_text_label = tk.Label(image_canvas, textvariable=image_text_var)
image_text_label.pack()
image_label = tk.Label(image_canvas)

def create_choice_button(a):
    tk.Radiobutton(quiz_page, textvariable=choices_vars[a], variable=chosen_var, value=a).pack()
[create_choice_button(i) for i in range(5)]

#####################

create_images()
create_choose_frame()

root.mainloop()