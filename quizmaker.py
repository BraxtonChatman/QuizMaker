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

    def change_title(self, new_title):
        """Change quiz title"""
        self.title = new_title

    def goto_q(self, num):
        """Change current question to the indicated question number, if valid"""
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
        self.type = ""
        self.q_text = ""
        self.answer = ""
        self.options = []

    def add_option(self):
        """Add an option to the options list"""

    def rem_option(self, option_index):
        """Remove an answer option from options list"""
        if option_index in range(len(self.options)):
            self.options.pop(option_index)

    def change_type(self, qtype):
        """Change self.type to qtype based on desired question response type"""
        self.type = qtype

    def set_correct(self):
        """Set which of the options in the options list are correct"""
        pass


class QuizGui(tk.Tk):
    """Class for GUI representation of Quiz"""

    def __init__(self):
        self.quiz = Quiz()

        tk.Tk.__init__(self)
        self.title("Quiz Maker")
        self.geometry("800x450")
        self.state("zoomed")

        self.window = tk.Frame(self)
        self.window.pack()

        # Menu bar ######################################################################
        main_menu = tk.Menu(self.window)
        self.config(menu = main_menu)

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

        # Label Frames ########################################################
        sidebar = tk.LabelFrame(self.window, text = "Question List", font = "bold")
        current_question = tk.LabelFrame(self.window, text = "Current Question", font = "bold")
        current_answer = tk.LabelFrame(self.window, text = "Answer", font = "bold")
        options = tk.LabelFrame(self.window, text = "Options", font = "bold")


        sidebar.pack(side="left", padx = 10, pady = 10)
        current_question.pack(pady = 10)
        current_answer.pack(pady = 10)
        options.pack(expand=True, fill = tk.X, pady = 10, ipady = 5)


        ## Sidebar ######################################################################
        self.side_scroll = tk.Scrollbar(sidebar)
        self.side_scroll.pack(side="right", fill = tk.Y, pady = (10, 0))
        self.scroll_list = tk.Listbox(sidebar, yscrollcommand=self.side_scroll.set, height = 25, width = 50)
        self.sidebar_list = []

        # for line in range(1, 10):
        #     sidebar_q = str(line)+ ". Question limited to 20".strip()[:20]+"..."+"     MC"
        #     self.scroll_list.insert(tk.END, sidebar_q)

        self.scroll_list.pack(side="left", pady = (10,0))
        self.side_scroll.config(command = self.scroll_list.yview)


        ## Question ######################################################################
        question_text = tk.Text(current_question, height = 6, width = 60)
        question_text.grid(row = 0, column = 0, columnspan = 2, pady = (5, 0))


        ## Answer ######################################################################
        answer_text = tk.Text(current_answer, height = 6, width = 60)
        response_type_label = tk.Label(current_answer, text = "Response Type")
        response_type = ttk.Combobox(current_answer, values = ["Multiple Choice", "Check All", "True or False", "Written Response"], state = "readonly")

        response_type_label.grid(row = 1, column = 1, pady = 5, sticky="e")
        response_type.grid(row = 1, column = 2, pady = 5)
        answer_text.grid(row =2, column = 0, columnspan=3)


        ## Options ######################################################################
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
            widget.configure(borderwidth = 3)
            widget.grid_configure(padx = 5, pady = (6, 3))


    def change_answer_window(self, answer_type):
        """change the answer window on the screen according to the response type"""
        pass

    def print_sidebar(self, quiz):
        """"""

    def add_sidebar(self, quiz):
        """add an indicated question to the screen sidebar"""
        current_question = quiz.current_q
        new_question = quiz.q_list[current_question].q_text

        sidebar_string = str(current_question) + new_question[:30] + "     " + quiz.q_list[current_question].type
        self.sidebar_list.insert(current_question, sidebar_string)
        self.scroll_list.insert(tk.END, self.sidebar_list[0])

    def rem_sidebar(self, question):
        """remove an indicated question from the screen sidebar"""
        pass

    def change_title(self):
        """change window title based on current quiz title"""
        if self.quiz.title:
            self.title("Quiz Maker:" + self.quiz.title)
        else:
            self.title("Quiz Maker: Untitled")


def filler_command():
    pass


if __name__ == "__main__":
    quizzer = QuizGui()

    my_question = Question()
    my_question.q_text = "What is my birthday"

    my_quiz = Quiz()
    my_quiz.q_list.append(my_question)
    my_quiz.current_q = 0

    quizzer.add_sidebar(my_quiz)


    quizzer.mainloop()



# TODO
# Working on add_sidebar function
# make test question and quiz for it

# then remove sidebar