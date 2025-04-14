import random
from tkinter import *
import pandas as pd

try:
    words_list = pd.read_csv('data/words_to_learn.csv').to_dict(orient="records")
except FileNotFoundError:
    words_list = pd.read_csv('words.csv').to_dict(orient="records")
finally:
    actualWord = random.choice(words_list)

# Cores
GREEN_BG = '#91c2af'
BG_COLOR = GREEN_BG

###############################################################################Functions
def right_option(_=None):  #recebe o evento se vier de tag_bind
    global actualWord,words_list
    desativar_botoes()
    change_cards()
    canvas.itemconfig(language_text, text='Portuguese')
    canvas.itemconfig(word_txt, text=actualWord['Portuguese'])

    words_list.remove(actualWord)
    new_data = pd.DataFrame(words_list)
    new_data.to_csv('data/words_to_learn.csv',index=False)

    tela.after(2000, newcard)

def wrong_option(_=None):
    global actualWord,words_list
    canvas.itemconfig(language_text, text='English')
    actualWord = random.choice(words_list)
    canvas.itemconfig(word_txt, text=actualWord['English'])

def change_cards():
    global BG_COLOR
    if BG_COLOR == GREEN_BG:
        canvas.itemconfig(language_text, text='Português')
        canvas.itemconfig(card_image, image=backcard_img)
        BG_COLOR = 'white'
    else:
        canvas.itemconfig(language_text, text='English')
        canvas.itemconfig(card_image, image=frontcard_img)
        BG_COLOR = GREEN_BG

    canvas.config(bg=BG_COLOR)
    tela.config(bg=BG_COLOR)

def newcard():
    global actualWord,words_list
    change_cards()
    canvas.itemconfig(language_text, text='English')
    actualWord = random.choice(words_list)
    canvas.itemconfig(word_txt, text=actualWord['English'])
    ativar_botoes()

def desativar_botoes():
    canvas.tag_unbind(ok_btn, "<Button-1>")
    canvas.tag_unbind(wrong_btn, "<Button-1>")

def ativar_botoes():
    canvas.tag_bind(ok_btn, "<Button-1>", right_option)
    canvas.tag_bind(wrong_btn, "<Button-1>", wrong_option)
##########################################################################################3
# Interface
tela = Tk()
tela.title('Flashcard Language Game')
tela.config(padx=10, pady=10, bg=BG_COLOR)

# Imagens
frontcard_img = PhotoImage(file="images/card_front.png")
backcard_img = PhotoImage(file="images/card_back.png")
rightbutton_img = PhotoImage(file="images/right.png")
wrongbutton_img = PhotoImage(file="images/wrong.png")

##################################################################### Ui Config
canvas = Canvas(width=800, height=650, bg=BG_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

card_image = canvas.create_image(400, 280, image=frontcard_img)
language_text = canvas.create_text(400, 150, text='Language', font=('Times New Roman', 26, 'italic'))
word_txt = canvas.create_text(400, 250, text=actualWord, font=('Times New Roman', 34, 'bold'))

#Botões como imagem e tag_bind
ok_btn = canvas.create_image(550, 590, image=rightbutton_img)
wrong_btn = canvas.create_image(250, 590, image=wrongbutton_img)
ativar_botoes()
##############################################################################################3
#Inicializa com uma palavra em ingles
wrong_option()

# loop da tela
tela.mainloop()
