import tkinter as tk
from tkinter import ttk

class Quiz():
    """Class representing the quiz. Contains list of Question objects as well as positional
    data and functions to modify questions."""

    def __init__(self):
        self.title = ""
        self.q_list = []
        self.length = 0
        self.current_q = None

    def change_title(self):
        pass

    def goto_q(self, num):
        pass

    def add_question(self, index):
        pass

    def del_question(self, index):
        pass

    def save_file(self):
        pass

    def read_file(self):
        pass

    def next_q(self):
        pass

    def prev_q(self):
        pass


class Question():
    """Class representing a question on the quiz. type represents what kind of response
    the question expects (Multiple choice, check all, true/false, or written), q_text represents
    the question text as a string, answer represents the answer text as a string for questions that
    have set answers (all but written response), options is a list of strings representing the available
    options to answer."""

    def __init__(self):
        self.type = None
        self.q_text = ""
        self.answer = ""
        self.options = []

    def add_option(self):
        pass

    def rem_option(self):
        pass


class QuizGui(tk.Tk):
    """Class for GUI representation of Quiz"""

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Quiz Maker")
        self.geometry("800x450")
        self.state("zoomed")


def filler_command():
    pass


quizzer = QuizGui()

window = tk.Frame(quizzer)
window.pack()


# Menu bar ###########################################################################
main_menu = tk.Menu(window)
quizzer.config(menu = main_menu)

file_menu = tk.Menu(main_menu, tearoff = 0)
edit_menu = tk.Menu(main_menu, tearoff = 0)
quiz_menu = tk.Menu(main_menu, tearoff = 0)

file_menu.add_command(label = "New Quiz", command= filler_command)
file_menu.add_command(label = "Open Quiz")
file_menu.add_command(label = "Save Quiz")
file_menu.add_command(label = "Save As")

edit_menu.add_command(label = "Change Question Order", command=filler_command)
edit_menu.add_command(label = "Add Question")
edit_menu.add_command(label = "Delete Question")
edit_menu.add_command(label = "Change Quiz Title")

quiz_menu.add_command(label = "Run Quiz")
quiz_menu.add_command(label = "Stop Quiz")
quiz_menu.add_command(label = "Question Weights")

main_menu.add_cascade(label = "File", menu = file_menu)
main_menu.add_cascade(label = "Edit", menu = edit_menu)
main_menu.add_cascade(label = "Quiz", menu = quiz_menu)


## Label Frames ########################################################
sidebar = tk.LabelFrame(window, text = "Question List", font = "bold")
current_question = tk.LabelFrame(window, text = "Current Question", font = "bold")
current_answer = tk.LabelFrame(window, text = "Answer", font = "bold")
options = tk.LabelFrame(window, text = "Options", font = "bold")


sidebar.pack(side="left", padx = 10, pady = 10)
current_question.pack(pady = 10)
current_answer.pack(pady = 10)
options.pack(expand=True, fill = tk.X, pady = 10, ipady = 5)


## Sidebar ##############################################################
side_scroll = tk.Scrollbar(sidebar)
side_scroll.pack(side="right", fill = tk.Y, pady = (10, 0))
scroll_list = tk.Listbox(sidebar, yscrollcommand=side_scroll.set, height = 25, width = 40)

for line in range(1, 200):
    scroll_list.insert(tk.END, "List item #"+str(line))

scroll_list.pack(side="left", pady = (10,0))
side_scroll.config(command = scroll_list.yview)


## Question #############################################################
question_text = tk.Text(current_question, height = 6, width = 60)
question_text.grid(row = 0, column = 0, columnspan = 2, pady = (5, 0))


## Answer ###############################################################
answer_label = tk.Label(current_answer, text = "Answer")
answer_text = tk.Text(current_answer, height = 6, width = 60)
response_type_label = tk.Label(current_answer, text = "Response Type")
response_type = ttk.Combobox(current_answer, values = ["Multiple Choice", "Check All", "True or False", "Written Response"], state = "readonly")

#answer_label.grid(row = 0, column = 0, columnspan=2)
response_type_label.grid(row = 1, column = 1, pady = 5, sticky="e")
response_type.grid(row = 1, column = 2, pady = 5)
answer_text.grid(row =2, column = 0, columnspan=3)


## Options ##############################################################
add_question_button = tk.Button(options, text = "Add Question")
del_question_button = tk.Button(options, text = "Delete Question")
prev_button = tk.Button(options, text = "Previous", width = 7)
next_button = tk.Button(options, text = "Next", width = 7)
save_button = tk.Button(options, text = "Save", width = 7)
fin_button = tk.Button(options, text = "Finish", width = 7)

prev_button.grid(row = 0, column = 0)
next_button.grid(row = 0, column = 1)
add_question_button.grid(row = 0, column = 2)
del_question_button.grid(row = 0, column = 3)
save_button.grid(row = 0, column = 4)
fin_button.grid(row = 0, column = 5)

for widget in options.winfo_children():
    widget.grid_configure(padx = 5, pady = (6, 3))





##

# true_label = tk.Label(work_window, text = "True:", font = "bold")
# true_text = tk.Text(work_window, height = 3, width = 50)
# false_label = tk.Label(work_window, text = "False:", font = "bold")
# false_text = tk.Text(work_window, height = 3, width = 50)

# true_label.grid(row = 3, column=0)
# true_text.grid(row = 3, column=1, columnspan=5, pady = 5)
# false_label.grid(row = 4, column=0)
# false_text.grid(row = 4, column=1, columnspan=5, pady = 5)



quizzer.mainloop()
# root.mainloop()



if __name__ == "__main__":
    pass
