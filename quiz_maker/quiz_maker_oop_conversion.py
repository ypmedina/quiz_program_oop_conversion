import tkinter as tk
from tkinter import Radiobutton, IntVar, messagebox
import os
import json

class TextEntry:
    def __init__(self, window, placeholder):
        self.frame = tk.Frame(window)
        self.frame.pack(padx=20, pady=10)

        self.label = tk.Entry(self.frame, width=15, font='Arial, 12', bd=1, relief='solid')
        self.label.pack(side='left')
        self.label.insert(0, placeholder)

        self.text = tk.Text(self.frame, height=1, width=50, font='Arial, 12', bd=1, relief='solid')
        self.text.pack(side='left')

    def get(self):
        return self.text.get("1.0", "end").strip()

    def clear(self):
        self.text.delete("1.0", "end")


class AnswerInput:
    def __init__(self, window, number, label, variable):
        self.frame = tk.Frame(window)
        self.frame.pack(padx=30, pady=10)

        self.text = tk.Text(self.frame, height=1, width=50, font="Arial, 12")
        self.text.pack(side='left')

        self.radio_but = Radiobutton(self.frame, variable=variable, value=number)
        self.radio_but.pack(side="left")

        self.letter = tk.Label(self.frame, text=label, font="Arial, 12")
        self.letter.pack(side="left")

    def get(self):
        return self.text.get("1.0", "end").strip()

    def clear(self):
        self.text.delete("1.0", "end")

class QuizManager:
    def __init__(self):
        self.questions = []

    def add_question(self, question_text, answers, correct):
        self.questions.append({
            "question": question_text,
            "answers": answers,
            "correct": correct
        })

    def save(self, name):
        data = {
            "name": name,
            "questions": self.questions
        }

        desktop_path = os.path.join(os.path.expanduser("~"), "Documents", "user_quiz_GUI.json")
        with open(desktop_path, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        return desktop_path

class QuizMaker:
    def __init__(self,root):
        self.root = root
        self.root.title("Quiz Maker")
        self.root.geometry("900x600")
        self.root.configure(bg="#fff9ed")

        self.radio_button = IntVar()
        self.quiz_manager = QuizManager()

        self.build_header()
        self.build_inputs()
        self.build_buttons()

    def build_header(self):
        header_frame = tk.Frame(self.root, height=50, bd=1, bg='#fff9ed')
        header_frame.pack(fill='x')
        header_label = tk.Label(header_frame, text='Quiz maker', font='Arial, 60', bg='#fff9ed')
        header_label.pack(anchor="w")

    def build_inputs(self):
        self.name_entry = TextEntry(self.root, "input name here: ")
        self.question_entry = TextEntry(self.root, "Input question here: ")

        self.answers = [
            AnswerInput(self.root, 1, "A", self.radio_button),
            AnswerInput(self.root, 2, "B", self.radio_button),
            AnswerInput(self.root, 3, "C", self.radio_button),
            AnswerInput(self.root, 4, "D", self.radio_button)
        ]

    def build_buttons(self):
        button_frame = tk.Frame(self.root, bg='#fff9ed')
        button_frame.pack(padx=40, pady=30)

        save_btn = tk.Button(button_frame, text="Save", command=self.save_button)
        save_btn.grid(row=0, column=0, pady=10, padx=20)

        stop_btn = tk.Button(button_frame, text="Stop", command=self.root.quit)
        stop_btn.grid(row=0, column=1, pady=10, padx=20)

        next_btn = tk.Button(self.root, text="next", command=self.next_button, width=20)
        next_btn.pack(anchor='center')


    def next_button(self):
        question = self.question_entry.get()
        answers = [answer.get() for answer in self.answers]
        correct = self.radio_button.get()

        if question and all(answers) and correct in [1, 2, 3, 4]:
            self.quiz_manager.add_question(question, answers, correct)

            self.question_entry.clear()
            for a in self.answers:
                a.clear()
            self.radio_button.set(0)
        else:
            messagebox.showwarning("Incomplete", "Please fill all fields and select the correct answer.")

    def save_button(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Missing Name", "Please enter a quiz name.")
            return

        path = self.quiz_manager.save(name)
        messagebox.showinfo("Saved", f"Quiz saved to: {path}")