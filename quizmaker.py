import tkinter as tk

def filler_command():
    pass


root = tk.Tk()
root.title("Quiz Maker")
root.geometry("400x400")

window = tk.Frame(root)
window.pack()

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

quiz_menu.add_command(label = "Run Quiz")
quiz_menu.add_command(label = "Stop Quiz")
quiz_menu.add_command(label = "Question Weights")


main_menu.add_cascade(label = "File", menu = file_menu)
main_menu.add_cascade(label = "Edit", menu = edit_menu)
main_menu.add_cascade(label = "Quiz", menu = quiz_menu)


root.mainloop()



if __name__ == "__main__":
    pass
