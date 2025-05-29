import tkinter as tk
from tkinter import messagebox
import os
import json
import random


class QuizProgram:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz program")
        self.root.geometry("700x400")
        self.bg_color= "#fff9ed"
        self.root.configure(bg= self.bg_color)

        self.quiz_data = self.load_quiz_data()
        self.questions = self.quiz_data["questions"]
        random.shuffle(self.questions)

        self.current_number = 0
        self.score = 0

        self.question_var = tk.StringVar()
        self.selected = tk.IntVar()
        self.answer_vars = [tk.StringVar() for _ in range(4)]

        self.user_interface()
        self.load_question()

    def load_quiz_data(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Documents", "user_quiz_GUI.json")
        try:
            with open(desktop_path, 'r', encoding='utf=8') as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "The quiz file could not be found.")
            self.root.destroy()
            exit()


    def user_interface(self):
        #Header
        header_frame = tk.Frame(self.root, height=50, bd=1, bg=self.bg_color)
        header_frame.pack(fill='x')
        header_label = tk.Label(header_frame, text='Quiz', font='Arial, 60', bg=self.bg_color)
        header_label.pack(anchor="w")

        #Questions
        tk.Label(self.root, textvariable=self.question_var, font=("Arial", 16),
                 bg=self.bg_color, wraplength=550).pack(pady=20)

        #Answers
        for i in range(4):
            tk.Radiobutton(self.root, textvariable=self.answer_vars[i], variable=self.selected,
                           value=i + 1, font=("Arial", 12), bg=self.bg_color).pack(anchor="w", padx=50)

        #Buttons
        button_frame = tk.Frame(self.root, bg='#fff9ed')
        button_frame.pack(padx=40, pady=30)

        tk.Button(button_frame, bg='#fff9ed', text="Next", command=self.next_question)\
            .grid(row=0, column=2, padx=20)

        tk.Button(button_frame, bg='#fff9ed', text="Stop", command=self.exit_button)\
            .grid(row=0, column=1, padx=20)


    def load_question(self):
        question_count = self.questions[self.current_number]
        self.question_var.set(f"Q{self.current_number + 1}: {question_count['question']}")
        for i in range(4):
            self.answer_vars[i].set(question_count["answers"][i])
        self.selected.set(0)


    def next_question(self):
        if self.selected.get() == self.questions[self.current_number]["correct"]:
            self.score += 1
        self.current_number += 1
        if self.current_number < len(self.questions):
            self.load_question()
        else:
            messagebox.showinfo("Quiz Complete",
                                f"{self.quiz_data['name']}'s Quiz\nScore: {self.score}/{len(self.questions)}")
            self.root.destroy()


    def exit_button(self):
        self.root.destroy()
        messagebox.showinfo("Stopped the quiz program", "Thank you for trying the quiz program! Have a good day")

