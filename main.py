from tkinter import *
import pandas
import pandas as pd
from random import *

BACKGROUND_COLOR = "#B1DDC6"
learn_data = {}

# ---------------------------- GET DATA ------------------------------- #
try:
    data = pd.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    ori_data = pd.read_csv('data/french_words.csv')
    learn_data = ori_data.to_dict(orient="records")
else:
    learn_data = data.to_dict(orient="records")
french = "French"
english = "English"
current_word = {}


def next_card():
    canvas.itemconfig(canvas_image, image=card_front)
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = choice(learn_data)
    canvas.itemconfig(card_title, text=french, fill='black')
    canvas.itemconfig(card_word, text=current_word[french], fill='black')
    flip_timer = window.after(3000, func=flip_card)


def next_card_right():
    learn_data.remove(current_word)
    new_data = pandas.DataFrame(learn_data)
    new_data.to_csv('data/words_to_learn.csv', index=False)
    next_card()


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(card_title, text=english, fill='white')
    canvas.itemconfig(card_word, text=current_word[english], fill='white')

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Image
card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")

canvas = Canvas(width=800, height=526)
canvas_image = canvas.create_image(405, 263, image=card_front)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

# Button
right_button = Button(image=right_img, highlightthickness=0, command=next_card_right)
right_button.grid(column=1, row=1)
wrong_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

next_card()

window.mainloop()
