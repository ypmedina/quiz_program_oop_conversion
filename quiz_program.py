import tkinter as tk
from tkinter import messagebox
import os
import json
import random

window = tk.Tk()

bg_color = "#fff9ed"
main_color = "#f5fcd1"
font_color = "#f5fcd1"

window.geometry("700x400")
window.configure(bg=bg_color)

header_frame = tk.Frame(window, height=50, bd=1, bg='#fff9ed')
header_frame.pack(fill='x')

header_label = tk.Label(header_frame, text='Quiz', font='Arial, 60', bg='#fff9ed')
header_label.pack(anchor="w")

desktop_path = os.path.join(os.path.expanduser("~"), "Documents", "user_quiz_GUI.json")

try:
    with open(desktop_path, 'r', encoding='utf=8') as file:
        quiz_data = json.load(file)

except FileNotFoundError:
    print("The file is not found. Please make sure to save the quiz")
    exit()


questions = quiz_data["questions"] #from kson
current_number = 0
score = 0
random.shuffle(questions)

question_var = tk.StringVar()
selected = tk.IntVar()
answer_vars = [tk.StringVar() for _ in range(4)]

def load_question():
    question_count = questions[current_number]
    question_var.set(f"Q{current_number+1}: {question_count['question']}")
    for i in range(4):
        answer_vars[i].set(question_count["answers"][i])
    selected.set(0)


def next_question():
    global current_number, score
    if selected.get() == questions[current_number]["correct"]:
        score += 1
    current_number += 1
    if current_number < len(questions):
        load_question()
    else:
        messagebox.showinfo("Quiz Complete", f"{quiz_data['name']}'s Quiz\nScore: {score}/{len(questions)}")
        window.destroy()

tk.Label(window, bg='#fff9ed' , textvariable=question_var, font=("Arial", 16), wraplength=550).pack(pady=20)


def exit_button():
    window.destroy()
    messagebox.showinfo("Stopped the quiz program", "Thank you for trying the quiz program! Have a good day")

for i in range(4):
    tk.Radiobutton(window,bg='#fff9ed', textvariable=answer_vars[i], variable=selected, value=i+1, font=("Arial", 12)).pack(anchor="w", padx=50)


button_frame = tk.Frame(window, bg='#fff9ed')
button_frame.pack(padx=40, pady=30)

next_btn = tk.Button(button_frame, bg='#fff9ed', text="Next", command=next_question)
next_btn.grid(row=0, column=2, pady=10, padx=20)

stop_btn = tk.Button(button_frame, bg='#fff9ed', text="Stop", command=exit_button)
stop_btn.grid(row=0, column=1, pady=10, padx=20)


load_question()
window.mainloop()