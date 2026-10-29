
import tkinter as tk
from tkinter import ttk, messagebox

# 10 MCQ questions: question, options, correct answer index
questions = [
    {
        "question": "1. What is the capital of India?",
        "options": ["Mumbai", "New Delhi", "Chennai", "Kolkata"],
        "answer": 1
    },
    {
        "question": "2. Which planet is known as the Red Planet?",
        "options": ["Earth", "Venus", "Mars", "Jupiter"],
        "answer": 2
    },
    {
        "question": "3. What is 12 × 8?",
        "options": ["88", "96", "108", "86"],
        "answer": 1
    },
    {
        "question": "4. Which language is used for this application?",
        "options": ["Java", "C++", "Python", "PHP"],
        "answer": 2
    },
    {
        "question": "5. How many days are there in a leap year?",
        "options": ["364", "365", "366", "367"],
        "answer": 2
    },
    {
        "question": "6. Which is the largest ocean?",
        "options": [
            "Atlantic Ocean",
            "Indian Ocean",
            "Arctic Ocean",
            "Pacific Ocean"
        ],
        "answer": 3
    },
    {
        "question": "7. Which gas do plants absorb?",
        "options": ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"],
        "answer": 1
    },
    {
        "question": "8. What is the extension of a Python file?",
        "options": [".html", ".java", ".py", ".cpp"],
        "answer": 2
    },
    {
        "question": "9. Which is the smallest prime number?",
        "options": ["0", "1", "2", "3"],
        "answer": 2
    },
    {
        "question": "10. How many sides does a hexagon have?",
        "options": ["5", "6", "7", "8"],
        "answer": 1
    }
]

# Store selected answers
selected_answers = []

# Main application window
root = tk.Tk()
root.title("MCQ Quiz Application")
root.geometry("750x700")
root.minsize(600, 500)

# Main heading
heading = ttk.Label(
    root,
    text="MCQ QUIZ APPLICATION",
    font=("Arial", 20, "bold")
)
heading.pack(pady=(15, 5))

subtitle = ttk.Label(
    root,
    text="Answer all 10 questions and submit your quiz.",
    font=("Arial", 11)
)
subtitle.pack(pady=(0, 10))

# Scrollable area
container = ttk.Frame(root)
container.pack(fill="both", expand=True, padx=20, pady=5)

canvas = tk.Canvas(container, highlightthickness=0)
scrollbar = ttk.Scrollbar(
    container, orient="vertical", command=canvas.yview
)

quiz_frame = ttk.Frame(canvas, padding=10)

window_id = canvas.create_window(
    (0, 0), window=quiz_frame, anchor="nw"
)

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))


def resize_quiz_frame(event):
    canvas.itemconfigure(window_id, width=event.width)


quiz_frame.bind("<Configure>", update_scroll_region)
canvas.bind("<Configure>", resize_quiz_frame)

# Create all questions and radio buttons
for i, question_data in enumerate(questions):
    selected = tk.IntVar(value=-1)
    selected_answers.append(selected)

    question_box = ttk.LabelFrame(
        quiz_frame,
        text=f"Question {i + 1}",
        padding=10
    )
    question_box.pack(fill="x", pady=7)

    question_label = ttk.Label(
        question_box,
        text=question_data["question"],
        font=("Arial", 11, "bold"),
        wraplength=620
    )
    question_label.pack(anchor="w", pady=(0, 8))

    for option_index, option in enumerate(question_data["options"]):
        radio = ttk.Radiobutton(
            question_box,
            text=option,
            variable=selected,
            value=option_index
        )
        radio.pack(anchor="w", pady=2)


# Final result area
result_label = ttk.Label(
    root,
    text="",
    font=("Arial", 15, "bold"),
    justify="center"
)
result_label.pack(pady=8)


def submit_quiz():
    # Check if all questions have been answered
    unanswered = [
        i + 1
        for i, answer in enumerate(selected_answers)
        if answer.get() == -1
    ]

    if unanswered:
        messagebox.showwarning(
            "Incomplete Quiz",
            "Please answer all questions before submitting.\n"
            "Unanswered questions: "
            + ", ".join(map(str, unanswered))
        )
        return

    # Calculate score
    score = 0

    for i, question_data in enumerate(questions):
        if selected_answers[i].get() == question_data["answer"]:
            score += 1

    percentage = (score / len(questions)) * 100

    # Display final marks
    result_label.config(
        text=f"Your Final Score: {score}/{len(questions)}\n"
             f"Percentage: {percentage:.0f}%",
        foreground="green" if score >= 5 else "red"
    )

    # Prevent changing answers after submission
    for widget in quiz_frame.winfo_children():
        for child in widget.winfo_children():
            if isinstance(child, ttk.Radiobutton):
                child.config(state="disabled")

    submit_button.config(state="disabled")

    messagebox.showinfo(
        "Quiz Result",
        f"Quiz submitted successfully!\n\n"
        f"Marks: {score}/{len(questions)}\n"
        f"Percentage: {percentage:.0f}%"
    )


def restart_quiz():
    for answer in selected_answers:
        answer.set(-1)

    result_label.config(text="")
    submit_button.config(state="normal")

    for widget in quiz_frame.winfo_children():
        for child in widget.winfo_children():
            if isinstance(child, ttk.Radiobutton):
                child.config(state="normal")

    canvas.yview_moveto(0)


# Buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=(0, 15))

submit_button = ttk.Button(
    button_frame,
    text="Submit Quiz",
    command=submit_quiz
)
submit_button.pack(side="left", padx=8)

restart_button = ttk.Button(
    button_frame,
    text="Restart Quiz",
    command=restart_quiz
)
restart_button.pack(side="left", padx=8)

# Start the application
root.mainloop()
