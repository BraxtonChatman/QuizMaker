import tkinter as tk
from tkinter import ttk

def filler_command():
    pass


root = tk.Tk()
root.title("Quiz Maker")
root.geometry("400x400")
root.state("zoomed")

window = tk.Frame(root)
window.pack()


# Menu bar ###########################################################################
main_menu = tk.Menu(window)
root.config(menu = main_menu)

file_menu = tk.Menu(main_menu, tearoff = 0)
edit_menu = tk.Menu(main_menu, tearoff = 0)
quiz_menu = tk.Menu(main_menu, tearoff = 0)

file_menu.add_command(label = "New Quiz", command= filler_command)
file_menu.add_command(label = "Open Quiz")
file_menu.add_command(label = "Save Quiz")
file_menu.add_command(label = "Save As")

edit_menu.add_command(label = "Edit Quiz", command=filler_command)
edit_menu.add_command(label = "Add Question")
edit_menu.add_command(label = "Delete Question")

quiz_menu.add_command(label = "Run Quiz")
quiz_menu.add_command(label = "Stop Quiz")
quiz_menu.add_command(label = "Question Weights")

main_menu.add_cascade(label = "File", menu = file_menu)
main_menu.add_cascade(label = "Edit", menu = edit_menu)
main_menu.add_cascade(label = "Quiz", menu = quiz_menu)


# question_label = tk.Label(work_window, text = "Question (1): ", font = "bold")
# question_label.grid(row = 1, column = 0, pady = (10, 40))
# question_text = tk.Text(work_window, width = 50, height = 3)
# question_text.grid(row = 1, column = 1, columnspan=5, pady = (10, 40))



# true_label = tk.Label(work_window, text = "True:", font = "bold")
# true_text = tk.Text(work_window, height = 3, width = 50)
# false_label = tk.Label(work_window, text = "False:", font = "bold")
# false_text = tk.Text(work_window, height = 3, width = 50)

# true_label.grid(row = 3, column=0)
# true_text.grid(row = 3, column=1, columnspan=5, pady = 5)
# false_label.grid(row = 4, column=0)
# false_text.grid(row = 4, column=1, columnspan=5, pady = 5)


# prev_button = tk.Button(work_window, text = "Previous", width = 7)
# next_button = tk.Button(work_window, text = "Next", width = 7)
# save_button = tk.Button(work_window, text = "Save", width = 7)
# del_button = tk.Button(work_window, text = "Delete Question")
# fin_button = tk.Button(work_window, text = "Finish", width = 7)

# prev_button.grid(row = 12, column = 1, sticky = "w")
# next_button.grid(row = 12, column = 2, sticky = "w")
# save_button.grid(row = 12, column=3, pady = 10, sticky = "e")
# del_button.grid(row = 12, column=4, pady = 10, sticky = "e")
# fin_button.grid(row=12, column=5, pady = 10, sticky = "e")


## Label Frames ########################################################
sidebar = tk.LabelFrame(window, text="Questions")
current_question = tk.LabelFrame(window, text = "Current Question")
current_answer = tk.LabelFrame(window, text = "Answer")

sidebar.grid(row = 0, column = 0, rowspan = 2)
current_question.grid(row = 0, column = 1)
current_answer.grid(row = 1, column = 1)


## Sidebar ##############################################################
temp_label = tk.Label(sidebar, text="Question 1")
temp_label2 = tk.Label(sidebar, text = "Question 2")

side_scroll = tk.Scrollbar(sidebar)
side_scroll.pack(side="right", fill = tk.Y)

my_list = tk.Listbox(sidebar, yscrollcommand=side_scroll.set)
for line in range(1, 23):
    my_list.insert(tk.END, "List item #"+str(line))

my_list.pack(side="left", fill = tk.BOTH)

side_scroll.config(command = my_list.yview)


## Question #############################################################
question_label = tk.Label(current_question, text = "Question")
question_text = tk.Text(current_question, height = 3, width = 50)

question_label.grid(row = 0, column = 0)
question_text.grid(row = 1, column = 0)



## Answer ###############################################################
answer_label = tk.Label(current_answer, text = "Answer")
answer_text = tk.Text(current_answer, height = 3, width = 50)
response_type_label = tk.Label(current_answer, text = "Response Type")
response_type = ttk.Combobox(current_answer, values = ["Multiple Choice", "Check All", "True or False", "Written Response"], state = "readonly")

#answer_label.grid(row = 0, column = 0, columnspan=2)
response_type_label.grid(row = 1, column = 1, pady = 5, sticky="e")
response_type.grid(row = 1, column = 2, pady = 5)
answer_text.grid(row =2, column = 0, columnspan=3)





root.mainloop()



if __name__ == "__main__":
    pass
