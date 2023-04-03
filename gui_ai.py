""" CSC111 Winter 2023 Course Project : Compel-O-Meter

Description
===========
This file contains the functions required to display an interactive user interface using the alternative ai model :)

Copyright
==========
This file is Copyright (c) 2023 Akshaya Deepak Ramachandran, Kashish Mittal, Maryam Taj and Pratibha Thakur
"""

import tkinter as tk
import analysis


def submit_name(event):
    """Return the analysis of the text inputted by the user based on the AI version of the model"""
    # save the text provided by the users
    text = name_entry.get("1.0", "end-1c")

    # analyse the text
    results = analysis.compellingness_description_ai(text)
    score = results[0]
    descrp = results[1], results[2], results[3], results[4], results[5]
    rtrn_txt = str(score) + '\n' + descrp[0] + "\n" + descrp[1] + "\n" + descrp[2] + "\n" + descrp[3] + "\n" + descrp[4]

    # return an analysis based on the text
    message_label.config(text=rtrn_txt)


# cretaing a window to allow users to interact with the data by allowing them to input text
window = tk.Tk()
window.title("Compel-O-Meter")
window_width = 800
window_height = 800
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.config(bg="black")

x_pos = (screen_width - window_width) // 2
y_pos = (screen_height - window_height) // 2

window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

# Set the grid row and column configuration to center all widgets
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)

display_text = "Please enter your text and then click the submit button below:"

# displaying the above text to provide users with instructions on how to use the interactive interface
name_label = tk.Label(window, text=display_text, font=("Helvetica", 20), bg="black", fg="white")
name_label.grid(row=0, column=0, padx=10, pady=(20, 10), sticky=tk.N + tk.S + tk.E + tk.W)

# creating a text box for the users to input their text into
name_entry = tk.Text(window, font=("Helvetica", 20), width=30, height=5, bg="grey")
name_entry.grid(row=1, column=0, padx=50, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

# creating the submit button that will allow the users to submit their text and will allow the program to analyse what
# they have typed
canvas = tk.Canvas(window, width=150, height=70, highlightthickness=0, bg="black")
canvas.grid(row=4, column=0, padx=10, pady=10)

rect_button = canvas.create_rectangle(10, 10, 140, 60, fill="black", outline="white", width=4)
canvas.tag_bind(rect_button, "<Button-1>", submit_name)

submit_button = canvas.create_text(75, 35, text="Submit", font=("Helvetica", 20), fill="white", anchor="center")
canvas.tag_bind(submit_button, "<Button-1>")

canvas.tag_bind(submit_button, "<Button-1>", submit_name)

message_label = tk.Label(window, text="Analysis will be returned here", font=("Helvetica", 20), bg="grey", fg="white",
                         wraplength=600)
message_label.grid(row=5, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

window.mainloop()
