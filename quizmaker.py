import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class Question():
    """Class representing a question on the quiz. type represents what kind of response
    the question expects (Multiple choice, check all, true/false, or written in two letter abbreviation),
    q_text represents the question text as a string, answer represents the answer text as a string for
    questions that have set answers (all but written response), options is a list of strings representing
    the available options to answer."""

    def __init__(self, type = "MC", text = ""):
        self.type = type
        self.q_text = text

        # multiple choice correct answer indicator and answer options
        self.mc_ans = 0
        self.mc_optn = ["", "", "", ""]

        # check all correct answer indicator and answer options
        self.ca_ans = [False, False, False, False]
        self.ca_optn = ["", "", "", ""]

        # True/False correct answer
        self.tf_ans = True

        # Written Response correct answer
        self.wr_ans = ""

    # TODO 
    def change_type(self, qtype):
        """Change self.type to qtype based on desired question response type"""
        self.type = qtype

    def set_correct(self):
        """Set which of the options in the options list are correct"""
        pass
    
    def add_option(self):
        """Add an option to the options list"""
        pass

    def rem_option(self, option_index):
        """Remove an answer option from options list"""
        if option_index in range(len(self.options)):
            self.options.pop(option_index)


class Quiz():
    """Class representing the quiz. Contains list of Question objects as well as positional
    data and functions to modify questions."""

    def __init__(self):
        self.title = ""
        self.q_list = [Question()]
        self.length = 1
        self.current_q = 0

    def add_question(self):
        """Adds a question to q_list after index current_q"""
        self.q_list.insert(self.current_q + 1, Question())
        self.current_q += 1
        self.length += 1
        return True

    def del_question(self, index):
        """Delete the current question"""
        if self.length > 1:
            self.q_list.pop(index)
            self.length -= 1

            if index <= self.current_q and self.current_q != 0:
                self.current_q -= 1
            return True
        
        else:
            return False

    def goto_q(self, num):
        """Change current question to the indicated question number, if valid"""
        self.current_q = num

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


    # TODO
    def change_title(self, new_title):
        """Change quiz title"""
        self.title = new_title

    def save_file(self, filename):
        pass

    def read_admin(self, filename):
        """Reads data from csv file indicated by filename to present quiz
        in admin(quiz creator) mode"""
        pass

    def read_user(self, filename):
        """Reads data from csv file indicated by filename to present quiz
        in user(quiz taker) mode"""
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
        self.current_answer = tk.LabelFrame(self.window, text = "Answer", font = "bold", width = 490, height = 220)
        self.options = tk.LabelFrame(self.window, text = "Options", font = "bold")

        self.window.pack()
        self.sidebar.pack(side="left", padx = 10, pady = 10)
        self.current_question.pack(pady = 10)
        self.current_answer.pack(pady = 10)
        self.options.pack(expand=True, fill = tk.X, pady = 10, ipady = 5)

        self.current_answer.grid_propagate(0)

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
        file_menu.add_command(label = "New Quiz", command= None)
        file_menu.add_command(label = "Open Quiz")
        file_menu.add_command(label = "Save Quiz")
        file_menu.add_command(label = "Save As")

        # Edit tab suboptions
        edit_menu.add_command(label = "Change Question Order", command=None)
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
        self.scroll_list = tk.Listbox(self.sidebar, yscrollcommand=self.side_scroll.set, height = 25, width = 50)

        self.side_scroll.pack(side="right", fill = tk.Y, pady = (10, 0))
        self.scroll_list.pack(side="left", pady = (10,0))

        self.side_scroll.config(command = self.scroll_list.yview)

        # listbox bindings that allow traversal, selection, and deletion with keys
        self.scroll_list.bind("<Double-Button-1>", lambda event: self.switch_s())
        self.scroll_list.bind("<Return>", lambda event: self.switch_s())
        self.scroll_list.bind("<Delete>", lambda event: self.delete_question(-2))
        self.scroll_list.bind("<FocusOut>", lambda event: self.scroll_list.select_clear(0, tk.END))

    def make_qframe(self):
        """Fill question frame"""
        self.question_text = tk.Text(self.current_question, height = 6, width = 60)
        self.question_text.grid(row = 0, column = 0, columnspan = 2, pady = (5, 0))

        # TODO
        self.question_text.bind("<FocusOut>", lambda event: self.refresh_question())

    def make_aframe(self):
        """Fill answer frame"""

        # response type dictionary
        self.resp_dict = {"MC":"Multiple Choice", "CA":"Check All", "T/F":"True or False", "WR":"Written Response",
                          "Multiple Choice":"MC", "Check All":"CA", "True or False":"T/F", "Written Response":"WR"}

        # response type combobox
        self.response_type_label = tk.Label(self.current_answer, text = "Response Type: ")
        self.response_type_values = ["Multiple Choice", "Check All", "True or False", "Written Response"]
        self.response_type_var = tk.StringVar()
        self.response_type_var.set("Written Response")
        self.response_type = ttk.Combobox(self.current_answer, values = self.response_type_values, state = "readonly", textvariable=self.response_type_var)
        self.response_type.bind("<<ComboboxSelected>>", lambda event: self.refresh_question())


        # written response answer space
        self.answer_text = tk.Text(self.current_answer, height = 9, width = 60)

        # true or false answer space
        self.tf_var = tk.BooleanVar()
        self.true_button = ttk.Radiobutton(self.current_answer, text = " True", value = True, variable = self.tf_var)
        self.false_button = ttk.Radiobutton(self.current_answer, text = " False", value = False, variable = self.tf_var)

        # multiple choice answer space
        self.mc_var = tk.StringVar()
        self.mc_entries = [tk.Entry(self.current_answer, width = 70) for i in range(5)]
        self.mc_buttons = [ttk.Radiobutton(self.current_answer, text="", value="1234"[i], variable=self.mc_var) for i in range(4)]

        # check all that apply answer space
        self.ca_vars = [tk.BooleanVar() for i in range(4)]
        self.ca_entries = [tk.Entry(self.current_answer, width = 70) for i in range(4)]
        self.ca_buttons = [tk.Checkbutton(self.current_answer, text = "", variable = self.ca_vars[i], onvalue=True, offvalue=False) for i in range(4)]

        # geo manage
        self.response_type_label.grid(row = 1, column = 1, pady = 5, padx = (90, 5))
        self.response_type.grid(row = 1, column = 2, pady = 5)

    def make_oframe(self):
        """Fill options frame"""
        self.add_question_button = tk.Button(self.options, text = "Add Question", command = lambda: self.add_question())
        self.del_question_button = tk.Button(self.options, text = "Delete Question", command = lambda: self.delete_question(-1))
        self.prev_button = tk.Button(self.options, text = "Previous", width = 7, command = lambda: self.switch_q(-2))
        self.next_button = tk.Button(self.options, text = "Next", width = 7, command = lambda: self.switch_q(-1))
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
        current_question = self.quiz.q_list[self.quiz.current_q]

        # question text 
        self.question_text.delete("1.0", tk.END)
        self.question_text.insert(tk.END, current_question.q_text)

        # question response type
        current_type = self.resp_dict[current_question.type]
        self.response_type_var.set(current_type)

        # clear previous response widget
        wlist = self.current_answer.winfo_children()
        for child in wlist[2:]:
            child.grid_forget()

        # question answer formatted for multiple choice, single selection
        if current_question.type == "MC":
            for i in range(4):
                self.mc_buttons[i].grid(row = i+2, column=0, pady = 5)
                self.mc_entries[i].grid(row = i+2, column=1, columnspan = 2, pady = 5)

                self.mc_entries[i].delete(0, tk.END)
                self.mc_entries[i].insert(tk.END, current_question.mc_optn[i])

                if i == current_question.mc_ans - 1:
                    self.mc_var.set(str(i + 1))

        # formatted for check all answer
        elif current_question.type == "CA":
            for i in range(4):
                self.ca_buttons[i].grid(row = i + 2, column = 0, pady = 5)
                self.ca_entries[i].grid(row = i + 2, column = 1, columnspan=2)

                self.ca_entries[i].delete(0, tk.END)
                self.ca_entries[i].insert(tk.END, current_question.ca_optn[i])

                if current_question.ca_ans[i]:
                    self.ca_vars[i].set(True)

        # formatted for true/false answer
        elif current_question.type == "T/F":
            self.true_button.grid(row = 2, column = 0, padx = 40, pady = (30, 15))
            self.false_button.grid(row = 3, column = 0, padx = 40, pady = 10)

            self.tf_var.set(current_question.tf_ans)

        # formatted for written response
        elif current_question.type == "WR":
            self.answer_text.grid(row = 2, column = 0, columnspan=3)

            current_answer = current_question.wr_ans
            self.answer_text.delete("1.0", tk.END)
            self.answer_text.insert(tk.END, current_answer)

    def refresh_question(self):
        """updates the question and answer frames based on question response type being changed
        and or when question text is edited"""

        # change current question type to selected combobox option type
        new_type = self.response_type_var.get()
        current_question = self.quiz.q_list[self.quiz.current_q]
        current_question.change_type(self.resp_dict[new_type])

        # update Question text based on question_text input
        new_text = self.question_text.get("1.0", tk.END)
        current_question.q_text = new_text

        # print question with new type
        self.print_question()
        self.refresh_sidebar()

    def add_question(self):
        """Inserts a new question into quiz list after the current one and
        switches focus to it"""

        self.quiz.add_question()
        self.print_question()
        self.refresh_sidebar()

    def delete_question(self, index):
        """Deletes the current question from list. Function is used as command
        function for delete button as well as a function bind for delete key on
        sidebar. input -1 as index to delete current question. input -2 as index
        to delete currently selected item on sidebar"""

        if index == -1:
            index = self.quiz.current_q

        if index == -2:
            selection = self.scroll_list.curselection()[0]
            index = selection
            print(index)

        # prompt user if they are sure they want to delete
        message_string = "Are you sure you would like to delete this question?\n\n        There's no getting it back once you do."
        del_text = self.quiz.q_list[index].q_text
        del_title = "Delete Question {}: ".format(index + 1) + del_text
        valid = messagebox.askyesnocancel(title=del_title, message=message_string)

        if not valid:
            return False
            
        self.quiz.del_question(index)
        self.print_question()
        self.refresh_sidebar()

        return True

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
                if "\n" in q.q_text[:40]:
                    n_index = q.q_text[:40].find("\n")
                    q_val = q.q_text[:n_index] + "..." + (" " * 10)
                else:
                    q_val = q.q_text[:40] + "..." + (" " * 10)
            else:
                if "\n" in q.q_text:
                    n_index = q.q_text.find("\n")
                    q_val = q.q_text[:n_index] + "..."
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

        self.scroll_list.select_clear(0, tk.END)
        self.scroll_list.select_set(self.quiz.current_q)
        self.scroll_list.activate(self.quiz.current_q)
    
    def switch_q(self, direction):
        """Command for 'next' and 'prev' buttons as well as for sidebar switching
        which shifts focus to next, previous, or selected question in quiz list
        and prints it. Direction is numeric index with -1 representing next, -2
        representing previous, and other values representing index for question
        in Quiz.q_list"""
        if direction == -1:
            self.quiz.next_q()
        
        elif direction == -2:
            self.quiz.prev_q()

        else:
            self.quiz.goto_q(direction)

        # print question and update sidebar highlight/active item
        self.print_question()
        self.scroll_list.select_clear(0, tk.END)
        self.scroll_list.select_set(self.quiz.current_q)
        self.scroll_list.activate(self.quiz.current_q)

    def switch_s(self):
        """Bind function for double click on item in sidebar listbox.
        Switches question focus to double clicked item"""
        selection = self.scroll_list.curselection()
        if selection:
            self.switch_q(selection[0])
            self.print_question()

    def save_admin(self, filename = ""):
        """Command function for save button that saves quiz data to csv
        file by calling quiz.save_file"""
        self.quiz.save_file(filename)


    # TODO
    def read_admin(self, filename):
        """QuizGui wrapper function to call quiz.read_admin"""
        pass

    def read_user(self, filename):
        """QuizGui wrapper function to call quiz.read_user"""
        pass

    def change_title(self):
        """change window title based on current quiz title"""
        if self.quiz.title:
            self.title("Quiz Maker:" + self.quiz.title)
        else:
            self.title("Quiz Maker: Untitled")

            


if __name__ == "__main__":
    quizzer = QuizGui()

    #### Test Questions #######################################################################################
    q1 = Question(text = "What is the first question?", type = "MC") #, response = "this one")
    q1.mc_optn = ["The next one", "this one", "the previous one", "none"]
    q1.mc_ans = 2
    
    q2 = Question(text = "What is a true false question?", type = "WR") #, response = "not this one")
    q2.wr_ans = "A true/false question is one that has a binary option being either True, or False."
    
    
    q3 = Question(text = "Who was there when you saw it happen besides Kyle?", type="CA") #, response="nobody else was there")
    q3.ca_optn = ["Maddie", "Luke", "Davie", "Allen"]
    q3.ca_ans = [True, False, True, True]
    
    q4 = Question(text = "I am hot", type = "T/F")
    q4.tf_ans = False
    

    q5 = Question(text = "when is my birthday?", type="MC")
    q5.mc_optn = ["June 18", "June 12", "June 0", "June 100"]
    q5.mc_ans = 1

    ##############################################################################################



    quizzer.quiz.q_list = [q1, q2, q3, q4, q5]
    quizzer.quiz.length = 5

    quizzer.print_sidebar()
    #quizzer.quiz.del_question(5)
    #quizzer.refresh_sidebar()


    quizzer.quiz.current_q = 0
    quizzer.print_question()




    quizzer.mainloop()



# TODO

# add title
# save data

""" 1. Title
    2. number of questions
    3. question formatting
        - type
        - question text
        - """

# adjust q_frame and a_frame font and box size
