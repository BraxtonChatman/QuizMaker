import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import json


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

    def change_type(self, qtype):
        """Change self.type to qtype based on desired question response type"""
        self.type = qtype

    def change_question(self, text):
        """Changes value of q_text to text"""
        self.q_text = text

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

    def change_title(self, new_title):
        """Change quiz title"""
        self.title = new_title

    def save(self, filename):
        """Save contents of Quiz to filename. First two lines of file are
        quiz name (name of file, including path) and length of quiz. The
        Questions in the quiz are then formatted and saved to the lines
        of the file."""
        
        with open(filename, "w") as f:
            f.write(filename + "\n")
            f.write(str(self.length) + "\n")

            for question in self.q_list:
                # format question data in list to be json formatted and written to file
                out_data = []
                out_data.append(question.type)
                out_data.append(question.q_text)
                out_data.append(question.mc_ans)
                out_data.append(question.mc_optn)
                out_data.append(question.ca_ans)
                out_data.append(question.ca_optn)
                out_data.append(question.tf_ans)
                out_data.append(question.wr_ans)

                json.dump(out_data, f)
                f.write("\n")               

    def read(self, filename):
        """Filename is passed to function to indicate which file to open
        quiz from. If file is properly formatted .txt file for quiz, then
        contents will be read into Quiz."""
        
        with open(filename, "r") as f:
            pathname = f.readline()[:-1]
            quiz_length = int(f.readline()[:-1])

            # read quiz title and length from first two lines of file
            self.title = os.path.basename(pathname)[:-4]
            self.length = int(quiz_length) 

            # delete current question list
            del(self.q_list[:])

            # iterate through remaining lines of file to read in Questions
            for line in f:
                line_data = json.loads(line)
                new_question = Question()

                new_question.type = line_data[0]
                new_question.q_text = line_data[1]
                new_question.mc_ans = line_data[2]
                new_question.mc_optn = line_data[3]
                new_question.ca_ans = line_data[4] 
                new_question.ca_optn = line_data[5]
                new_question.tf_ans = line_data[6] 
                new_question.wr_ans = line_data[7]

                self.q_list.append(new_question)


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

        # file location variable for saving
        self.file_location = ""

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
        file_menu.add_command(label = "Open Quiz", command = self.read)
        file_menu.add_command(label = "Save", command=self.save)
        file_menu.add_command(label = "Save As", command=lambda: self.save(save_as=True))
        
        # Edit tab suboptions
        edit_menu.add_command(label = "Change Question Order", command=None)
        edit_menu.add_command(label = "Add Question")
        edit_menu.add_command(label = "Delete Question")
        edit_menu.add_command(label = "Change Quiz Title")

        # Quiz tab suboptions
        quiz_menu.add_command(label = "Run Quiz")
        quiz_menu.add_command(label = "Stop Quiz")
        quiz_menu.add_command(label = "Question Weights")

        # Enable saving through hotkey Control+s and Control+Shift+S
        self.bind("<Control-s>", self.save)
        self.bind("<Control-Shift-S>", lambda event: self.save(save_as=True))

        # Enable file opening through hotkey Control+o
        self.bind("<Control-o>", lambda event: self.read())

        # Enable question adding through hotkey Control+a
        self.bind("<Control-a>", lambda event: self.add_question())

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
        self.tf_var.set(True)
        self.true_button = ttk.Radiobutton(self.current_answer, text = " True", value = True, variable = self.tf_var)
        self.false_button = ttk.Radiobutton(self.current_answer, text = " False", value = False, variable = self.tf_var)

        # multiple choice answer space
        self.mc_var = tk.StringVar()
        self.mc_var.set("1")
        self.mc_entries = [tk.Entry(self.current_answer, width = 70) for i in range(5)]
        self.mc_buttons = [ttk.Radiobutton(self.current_answer, text="", value="1234"[i], variable=self.mc_var) for i in range(4)]

        # check all that apply answer space
        self.ca_vars = [tk.BooleanVar() for i in range(4)]
        for var in self.ca_vars:
            var.set(False)
        self.ca_entries = [tk.Entry(self.current_answer, width = 70) for i in range(4)]
        self.ca_buttons = [tk.Checkbutton(self.current_answer, text = "", variable = self.ca_vars[i], onvalue=True, offvalue=False) for i in range(4)]

        # update Question answer values when focus leaves answer widgets
        for widget in self.current_answer.winfo_children():
            widget.bind("<FocusOut>", lambda event: self.refresh_question())

        # geo manage
        self.response_type_label.grid(row = 1, column = 1, pady = 5, padx = (90, 5))
        self.response_type.grid(row = 1, column = 2, pady = 5)

    def make_oframe(self):
        """Fill options frame"""
        self.add_question_button = tk.Button(self.options, text = "Add Question", command = lambda: self.add_question())
        self.del_question_button = tk.Button(self.options, text = "Delete Question", command = lambda: self.delete_question(-1))
        self.prev_button = tk.Button(self.options, text = "Previous", width = 7, command = lambda: self.switch_q(-2))
        self.next_button = tk.Button(self.options, text = "Next", width = 7, command = lambda: self.switch_q(-1))
        self.save_button = tk.Button(self.options, text = "Save", width = 7, command = self.save)
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
        """Updates the question and answer frames based on question response type being changed
        and or when question text is edited, and updates Question based on changes"""

        current_question = self.quiz.q_list[self.quiz.current_q]
        current_type = current_question.type

        # update Question text based on question_text input
        new_text = self.question_text.get("1.0", tk.END)
        current_question.change_question(new_text)

        # update Question answer values when answer frame values are changed
        if current_type == "MC":
            for i in range(4):
                current_question.mc_optn[i] = self.mc_entries[i].get()
                if int(self.mc_var.get()) == i + 1:
                    current_question.mc_ans = i - 1

        elif current_type == "CA":
            for i in range(4):
                current_question.ca_ans[i] = self.ca_vars[i].get()
                current_question.ca_optn[i] = self.ca_entries[i].get()

        elif current_type == "T/F":
            new_answer = self.tf_var.get()
            current_question.tf_ans = new_answer

        elif current_type == "WR":
            new_answer = self.answer_text.get("1.0", tk.END)
            current_question.wr_ans = new_answer
            
        # change current question type to selected combobox option type
        new_type = self.resp_dict[self.response_type_var.get()]
        current_question.change_type(new_type)

        # print question with new type
        self.print_question()
        self.refresh_sidebar()

    def clear_answers(self):
        """Clear the answer widget values to be used before
        adding or switching question"""
        
        self.answer_text.delete("1.0", tk.END)
        self.tf_var.set(True)
        self.mc_var.set("1")
        for i in range(4):
            self.ca_vars[i].set(False)
            self.ca_entries[i].delete(0, tk.END)

    def add_question(self):
        """Inserts a new question into quiz list after the current one and
        switches focus to it"""

        # clear answer widget values before adding blank question
        self.clear_answers()     

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

        # update Question answer values, then clear question gui widget values
        self.refresh_question()
        self.clear_answers()

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

    def save(self, save_as = False):
        """Command and bind command for Save options (including Ctrl+s)
        that prompts the user for a filename to save the quiz in and calls
        to the Quiz.save method to write the contents of the Quiz to a file
        with selected name."""

        # input new name for save file if quiz has not been named yet or "save as" has been selected
        cwd = os.getcwd()
        if self.quiz.title == "" or save_as == True:
            save_filename = filedialog.asksaveasfilename(defaultextension=".txt", initialdir=cwd, filetypes=(("Text File", "*.txt"),))
            
            # add a .txt extension if an alternative extension was input
            if save_filename[-4:] != ".txt":
                save_filename += ".txt"

            # update self.file_location for future saves
            self.file_location = save_filename

            # use only the filename without path or extension for the quiz title
            new_title = os.path.basename(save_filename)[:-4]
            self.change_title(new_title)

        # pass save file name to quiz.save for file write
        self.quiz.save(self.file_location)

    def read(self):
        """QuizGui wrapper function to call quiz.read Prompts the
        user to select a file to open a quiz from. The file must be
        a properly formatted .txt file, and will be read into Quiz
        as well as update the sidebar, current question, and window title."""
        
        cwd = os.getcwd()
        open_filename = filedialog.askopenfilename(initialdir=cwd)
        if open_filename:
            self.quiz.read(open_filename)
            self.print_question()
            self.refresh_sidebar()

            self.change_title()

    def change_title(self, new_title = ""):
        """change window title based on current quiz title"""
       
        # get title from quiz if no title was input
        if new_title == "":
            new_title = self.quiz.title
        else:
            self.quiz.change_title(new_title)

        # if no title, window title stays "Quiz Maker" otherwise quiz title too
        if new_title == "":
            self.title("Quiz Maker")
        else:
            self.title("Quiz Maker: " + self.quiz.title)      

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

    #quizzer.quiz.q_list = [q1, q2, q3, q4, q5]
    #quizzer.quiz.length = 5

    quizzer.print_sidebar()
    #quizzer.quiz.del_question(5)
    #quizzer.refresh_sidebar()

    #quizzer.quiz.current_q = 0
    quizzer.print_question()
    

    quizzer.mainloop()

# TODO



# open appears to be adding questions

# loading rn.txt, adding question, and changing type to wr had prefilled answer text

# error check open wrong file types

# work on QuizGui save method

# add title
# save data

""" 1. Title
    2. number of questions
    3. question formatting
        - type
        - question text
        - """

# adjust q_frame and a_frame font and box size
