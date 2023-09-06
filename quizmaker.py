import tkinter as tk
from tkinter import ttk


class Quiz():
    """Class representing the quiz. Contains list of Question objects as well as positional
    data and functions to modify questions."""

    def __init__(self):
        self.title = ""
        self.q_list = [Question()]
        self.length = 1
        self.current_q = 0

    def change_title(self, new_title):
        """Change quiz title"""
        self.title = new_title

    def goto_q(self, num):
        """Change current question to the indicated question number, if valid"""
        self.current_q = num

    def add_question(self):
        """Adds a question to q_list after index current_q"""
        self.q_list.insert(self.current_q + 1, Question())
        self.length += 1
        return True

    def del_question(self, index):
        """Delete the current question"""
        if self.length > 1:
            self.q_list.pop(index - 1)
            self.length -= 1
            return True
        else:
            return False
        
    def next_q(self):
        """Moves question focus to the next question in q_list if it exists"""
        if self.current_q < self.length - 1:
            self.current_q += 1
        return self.current_q

    def prev_q(self):
        """Moves question focus to the previous question in q_list if it exists"""
        if self.current_q > 0:
            self.current_q -= 1
        return self.current_q

    def save_file(self):
        pass

    def read_file(self):
        pass


class Question():
    """Class representing a question on the quiz. type represents what kind of response
    the question expects (Multiple choice, check all, true/false, or written), q_text represents
    the question text as a string, answer represents the answer text as a string for questions that
    have set answers (all but written response), options is a list of strings representing the available
    options to answer."""

    def __init__(self, text = "", type = "", response = "", resp_list = []):
        self.type = type
        self.q_text = text
        self.answer = response
        self.options = resp_list

    def add_option(self):
        """Add an option to the options list"""
        pass

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
        # initialize root and main window
        tk.Tk.__init__(self)
        self.title("Quiz Maker")
        self.geometry("800x450")
        self.state("zoomed")

        # Quiz variable of GUI
        self.quiz = Quiz()

        # main window and label frames
        self.window = tk.Frame(self)
        self.sidebar = tk.LabelFrame(self.window, text = "Question List", font = "bold")
        self.current_question = tk.LabelFrame(self.window, text = "Current Question", font = "bold")
        self.current_answer = tk.LabelFrame(self.window, text = "Answer", font = "bold")
        self.options = tk.LabelFrame(self.window, text = "Options", font = "bold")

        self.window.pack()
        self.sidebar.pack(side="left", padx = 10, pady = 10)
        self.current_question.pack(pady = 10)
        self.current_answer.pack(pady = 10)
        self.options.pack(expand=True, fill = tk.X, pady = 10, ipady = 5)

        # Generate menu and content of labelframes in window
        self.make_menu()
        self.make_sframe()
        self.make_qframe()
        self.make_aframe()
        self.make_oframe()

    def make_menu(self):
        """Creates the menu bar and options at the top of the screen"""
        self.main_menu = tk.Menu(self.window)
        self.config(menu = self.main_menu)

        # Menu options "File", "Edit", "Quiz"
        file_menu = tk.Menu(self.main_menu, tearoff = 0)
        edit_menu = tk.Menu(self.main_menu, tearoff = 0)
        quiz_menu = tk.Menu(self.main_menu, tearoff = 0)
        self.main_menu.add_cascade(label = "File", menu = file_menu)
        self.main_menu.add_cascade(label = "Edit", menu = edit_menu)
        self.main_menu.add_cascade(label = "Quiz", menu = quiz_menu)

        # File tab suboptions
        file_menu.add_command(label = "New Quiz", command= filler_command)
        file_menu.add_command(label = "Open Quiz")
        file_menu.add_command(label = "Save Quiz")
        file_menu.add_command(label = "Save As")

        # Edit tab suboptions
        edit_menu.add_command(label = "Change Question Order", command=filler_command)
        edit_menu.add_command(label = "Add Question")
        edit_menu.add_command(label = "Delete Question")
        edit_menu.add_command(label = "Change Quiz Title")

        # Quiz tab suboptions
        quiz_menu.add_command(label = "Run Quiz")
        quiz_menu.add_command(label = "Stop Quiz")
        quiz_menu.add_command(label = "Question Weights")

    def make_sframe(self):
        """Fill sidebar frame"""
        self.side_scroll = tk.Scrollbar(self.sidebar)
        self.side_scroll.pack(side="right", fill = tk.Y, pady = (10, 0))
        self.scroll_list = tk.Listbox(self.sidebar, yscrollcommand=self.side_scroll.set, height = 25, width = 50)
        self.sidebar_list = []

        self.scroll_list.pack(side="left", pady = (10,0))
        self.side_scroll.config(command = self.scroll_list.yview)

    def make_qframe(self):
        """Fill question frame"""
        question_text = tk.Text(self.current_question, height = 6, width = 60)
        question_text.grid(row = 0, column = 0, columnspan = 2, pady = (5, 0))

    def make_aframe(self):
        """Fill answer frame"""
        answer_text = tk.Text(self.current_answer, height = 6, width = 60)
        response_type_label = tk.Label(self.current_answer, text = "Response Type")
        response_type = ttk.Combobox(self.current_answer, values = ["Multiple Choice", "Check All", "True or False", "Written Response"], state = "readonly")

        response_type_label.grid(row = 1, column = 1, pady = 5, sticky="e")
        response_type.grid(row = 1, column = 2, pady = 5)
        answer_text.grid(row =2, column = 0, columnspan=3)

    def make_oframe(self):
        """Fill options frame"""
        self.add_question_button = tk.Button(self.options, text = "Add Question")
        self.del_question_button = tk.Button(self.options, text = "Delete Question")
        self.prev_button = tk.Button(self.options, text = "Previous", width = 7)
        self.next_button = tk.Button(self.options, text = "Next", width = 7)
        self.save_button = tk.Button(self.options, text = "Save", width = 7)
        self.fin_button = tk.Button(self.options, text = "Finish", width = 7)

        self.prev_button.grid(row = 0, column = 0)
        self.next_button.grid(row = 0, column = 1)
        self.add_question_button.grid(row = 0, column = 2)
        self.del_question_button.grid(row = 0, column = 3)
        self.save_button.grid(row = 0, column = 4)
        self.fin_button.grid(row = 0, column = 5)

        for widget in self.options.winfo_children():
            widget.configure(borderwidth = 3)
            widget.grid_configure(padx = 5, pady = (6, 3))

    def print_question(self):
        """Display the currently selected Question in the GUI question and answer frames"""
        pass

    def print_sidebar(self):
        """Iterates through quiz.q_list and formats question data on screen sidebar"""
        index = 0
        for q in self.quiz.q_list:
            # question number
            index += 1
            q_num = str(index) + ". "
            if len(q_num) == 3:
                q_num += " "

            # question text 
            if len(q.q_text) > 39:
                q_val = q.q_text[:40] + "..." + (" " * 10)
            else:
                q_val = q.q_text
              
            # question type 
            q_type = "[" + q.type + "] "
            
            # question details formated string for sidebar
            sidebar_q = q_num + q_type + q_val
            self.scroll_list.insert(tk.END, sidebar_q)

    def refresh_sidebar(self):
        """Updates the sidebar by clearing and reinserting questions from the list"""
        self.scroll_list.delete(0, tk.END)
        self.print_sidebar()

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

    q1 = Question(text = "What is the first question?", type = "MC")
    q2 = Question(text = "What is a true false question?", type = "WR")
    q3 = Question(text = "Who was there when you saw it happen besides Kyle?", type="CA")
    q4 = Question(text = "I am hot", type = "T/F")
    q5 = Question(text = "when is my birthday?", type="MC")

    quizzer.quiz.q_list = [q1, q2, q3, q4, q5]
    quizzer.quiz.length = 5

    quizzer.print_sidebar()
    quizzer.quiz.del_question(5)
    quizzer.refresh_sidebar()

    quizzer.mainloop()



# TODO

# QuizGui.print_question
    # called whenever Quiz.add, .next, .prev, .goto_q
    # updates answer and question frames

# quiz.del_question index value