import inferior
import tkinter as tk
from tkinter import ttk
import random
from PIL import ImageTk, Image
import os
import time

# https://stackoverflow.com/questions/19860047/python-tkinter-scrollbar-for-entire-window

units = [int(x.replace('U>', '')) for x in inferior.units_indexes.keys()]

root = tk.Tk()
#root.configure(background='#999999')
root.title('APHG Progress Checks Practice')
root.geometry('1000x800')

###########

quiz_canvas = tk.Canvas(root, bg='#FF0000')
quiz_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

quiz_scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=quiz_canvas.yview)
quiz_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

quiz_canvas.configure(yscrollcommand=quiz_scrollbar.set)
quiz_canvas.bind('<Configure>', lambda e: quiz_canvas.configure(scrollregion=quiz_canvas.bbox('all')))

quiz_frame = tk.Frame(quiz_canvas)

quiz_canvas.create_window((0, 0), window=quiz_frame, anchor='nw')
#

def change_frame(a):
    quiz_canvas.event_generate('<Configure>')
    print(a)

def start_frame_pack():
    start_frame.pack()
    change_frame('start frame')

def question_frame_pack():
    question_frame.pack()
    change_frame('question frame')
        
def question_result_frame_pack():
    question_result_frame.pack()
    change_frame('question result frame')

def final_result_frame_pack():
    final_result_frame.pack()
    change_frame('final result frame')

start_frame = tk.Frame(quiz_frame, highlightbackground='#00FF00')
question_frame = tk.Frame(quiz_frame)
question_result_frame = tk.Frame(quiz_frame)
final_result_frame = tk.Frame(quiz_frame)

def create_start_frame():
    tk.Label(start_frame, text='APHG Progress Checks', font=('Noto Sans', 44, 'bold')).pack()

    create_choose_frame()

    start_frame_pack()

def create_choose_frame():
    global chosen; chosen = []

    choose_frame = tk.Canvas(start_frame); choose_frame.pack()

    tk.Button(choose_frame, text='Begin Practice', font=('Arial', 20), command=begin).pack(pady=10)

    [create_unit_button(unit, choose_frame) for unit in units]

def create_unit_button(unit, choose_frame):
    global chosen; chosen.append(tk.IntVar())

    tk.Checkbutton(choose_frame, text=f'Unit {unit}', font=('Arial', 15), variable=chosen[-1], onvalue=1, offvalue=0).pack(pady=5)

###################

def get_questions_lines():
    global questions_lines, images; questions_lines = []
    for i, unit_var in enumerate(chosen, start=1):
        if unit_var.get() == 1:
            unit_lines = inferior.get_unit_lines(i)
            questions_lines += inferior.get_questions_lines(unit_lines)
            unit_var.set(0)
    random.shuffle(questions_lines)

##########################################
# IMAGES #

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

##########################################

def set_result():
    result_var.set(f'Total Correct: {total_correct} | Total Incorrect: {total_incorrect} | Questions Completed: {total_correct+total_incorrect} | Total Questions: {len(questions_lines)}')

def begin():
    get_questions_lines()

    if len(questions_lines) > 0:
        global total_correct, total_incorrect; total_correct, total_incorrect = 0, 0
        question_num_var.set(1)
        set_result()

        start_frame.pack_forget()

        update_question(question_num_var.get())
##

def submit_question():
	question_frame.pack_forget()

	global total_correct, total_incorrect
	if chosen_var.get() != -1 and choices_vars[chosen_var.get()].get() == correct_choice[0]: 
		total_correct += 1
	else: 
		total_incorrect += 1
		topic = question_topic_var.get()
		if topic in incorrect_topics:
			incorrect_topics[topic] += 1
		else:
			incorrect_topics[topic] = 1
	set_result()
	
	# Result Page
	for i in range(5):
		is_correct_choice = choices_vars[i].get() == correct_choice[0]
		fg_color = '#0c6107' if is_correct_choice else '#bf1f02'
		bg_color = ('#d1ffbd' if is_correct_choice else '#f9aeae') if i == chosen_var.get() else '#F0F0F0'
		result_choices[i][0].config(fg=fg_color, bg=bg_color)
		result_choices[i][1].config(fg=fg_color, bg=bg_color)
	question_result_frame_pack()

def end_quiz():
    global incorrect_topics
    topics = sorted(incorrect_topics.items(), key=lambda x: x[1], reverse=True)
    incorrect_topics = {}

    quiz_grade = f'{round(total_correct/len(questions_lines)*100, 2)}%'
    final_result_label.config(text=f'Grade: {quiz_grade} ({total_correct}/{len(questions_lines)})')

    topics_text = '\n'.join([f'{topic} - {count}/3 Incorrect' for topic, count in topics])
    topics_label.config(text=topics_text)

    question_frame.pack_forget()
    final_result_frame_pack()

def next_question():
    question_result_frame.pack_forget()

    question_num = question_num_var.get()+1
    question_num_var.set(question_num)

    if question_num <= len(questions_lines):
        update_question(question_num)
    else: 
        end_quiz()

def update_question(question_num):
    chosen_var.set(-1)

    question_parts = inferior.get_question(questions_lines[question_num-1])

    question_label_var.set(question_parts[0])
    question_part_var.set(question_parts[3])
    question_topic_var.set(question_parts[4])

    image_parts = question_parts[5]
    if len(image_parts) != 0:
        image_label.pack()
        image_label.config(image=images[image_parts[0]])
        image_text_var.set(image_parts[1] if len(image_parts) == 2 else '')
    else: image_label.pack_forget()

    global correct_choice, incorrect_choices; correct_choice, incorrect_choices = question_parts[1], question_parts[2]
    all_choices = [correct_choice] + incorrect_choices; random.shuffle(all_choices)

    # Change Choice Variables
    for i in range(5): 
        choice_parts = all_choices[i]
        choices_vars[i].set(choice_parts[0])
        correct_incorrect = 'Correct' if choice_parts[0] == correct_choice[0] else 'Incorrect'
        choices_explanations_vars[i].set(f'{correct_incorrect}. {choice_parts[1]}')

    question_frame_pack()

##################### QUESTION PAGE ################################## 

## VARS
result_var = tk.StringVar()

question_num_var = tk.IntVar()
question_label_var = tk.StringVar()

image_text_var = tk.StringVar()

chosen_var = tk.IntVar()

choices_vars = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
choices_explanations_vars = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]

top_button_font = ('Noto Sans', 10, 'bold')
##

# Result Label
tk.Label(quiz_frame, textvariable=result_var).pack()

# Submit Button
submit_button = tk.Button(question_frame, text='Submit', font=top_button_font, width=8, command=submit_question)
submit_button.pack()

# Question Number Label
tk.Label(question_frame, textvariable=question_num_var, font=('Noto Sans', 13, 'bold')).pack(pady=5)

# Question Label
tk.Label(question_frame, textvariable=question_label_var, font=('Noto Sans', 11, 'bold'), wraplength=900).pack()

# Image Canvas
image_canvas = tk.Canvas(question_frame)
image_canvas.pack(pady=10)
tk.Label(image_canvas, textvariable=image_text_var, font=('Noto Sans', 10, 'bold')).pack()
image_label = tk.Label(image_canvas)

# Choices Canvas
choices_canvas = tk.Canvas(question_frame)
choices_canvas.pack()

def create_choice_button(a):
    tk.Radiobutton(choices_canvas, textvariable=choices_vars[a], font=('Noto Sans', 11), wraplength=900, variable=chosen_var, value=a).grid(row=a)
[create_choice_button(i) for i in range(5)]

######################### QUESTION RESULT PAGE ##################################

## VARS
question_part_var = tk.StringVar()
question_topic_var = tk.StringVar()
##

tk.Button(question_result_frame, text='Continue', font=top_button_font, width=10, command=next_question).pack()

# Question Number Label
tk.Label(question_result_frame, textvariable=question_num_var, font=('Noto Sans', 13, 'bold')).pack(pady=5)

# Part
tk.Label(question_result_frame, textvariable=question_part_var).pack()

# Topic
incorrect_topics = {}
tk.Label(question_result_frame, textvariable=question_topic_var).pack()
##

#######

def create_choice_explanations(i):
    choice_label = tk.Label(question_result_frame, textvariable=choices_vars[i], font=('Noto Sans', 10, 'bold'), wraplength=900)
    choice_label.pack(pady=5)
    choice_explanation_label = tk.Label(question_result_frame, textvariable=choices_explanations_vars[i], font=('Noto Sans', 9), wraplength=900)
    choice_explanation_label.pack()
    return [choice_label, choice_explanation_label]
result_choices = [create_choice_explanations(i) for i in range(5)]

######################### FINAL RESULT PAGE ##################################

def exit():
    final_result_frame.pack_forget()
    question_frame.pack_forget()
    start_frame_pack()

exit_results_button = tk.Button(final_result_frame, text='Exit', font=top_button_font, command=exit)
exit_results_button.pack()

final_result_label = tk.Label(final_result_frame)
final_result_label.pack()

tk.Label(final_result_frame, text='Topics to Study').pack()

topics_label = tk.Label(final_result_frame)
topics_label.pack()

###################################################

create_images()

create_start_frame()

root.mainloop()