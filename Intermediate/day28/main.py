import math
from tkinter import *
FONT_NAME = "Courier"
BG_COLOR = '#bbd8a3'
CICLE_MINS = 25
SHORTBREAK_MINS = 8
LONGBREAK_MINS = 15
reps = 0
timer = None
##############################################################FUNCTIONS
def reset_timer():
    tela.after_cancel(timer)
    title.config(text='Pomodoro Timer',fg='black')
    check_marks.config(text='')
    canvas.itemconfig(timer_txt,text='00:00')
    global reps
    reps = 0
def call_timer():
    global reps
    reps += 1
    if reps in [1,3,5,7]: #worktime full cicle red color
        print('worktime')
        timer_countdown(round(CICLE_MINS*60))
        title.config(text='Counting...',fg='#F75A5A')

    elif reps in [2,4,6]: #shortbreaks cicle yellow color
        print('shortbreaks')
        timer_countdown(round(SHORTBREAK_MINS*60))
        title.config(text='Resting Time...', fg='#FF9B17')

    elif reps == 8: #longbreak cicle blue color
        print('longbreak')
        timer_countdown(round(LONGBREAK_MINS*60))
        title.config(text='Long Rest Time...', fg='#3D90D7')

    else: #reset all
        print('reset reps')
        title.config(text='Pomodoro Timer', fg='black')
        check_marks.config(text='')
        reps = 0

def timer_countdown(count):

    countmins = math.floor(count/60)
    countsecs = count % 60
    if countmins < 10:
        countmins = f'0{countmins}'

    if countsecs < 10:
        countsecs = f"0{countsecs}"

    canvas.itemconfig(timer_txt,text=f'{countmins}:{countsecs}')
    if count > 0:
        global timer
        timer = tela.after(1000,timer_countdown,count-1)
    else:
        call_timer()
        marks = ''
        for cicle in range(math.floor(reps/2)):
            marks += '\n✔'
            check_marks.config(text=marks)
###########################################################User Interface
tela = Tk()
tela.title('Pomodoro Aplication')
tela.minsize(400,400)
tela.config(padx=10,pady=10,bg=BG_COLOR)

title = Label(text='Pomodoro Timer',bg=BG_COLOR,font=(FONT_NAME,22,'bold'))
title.grid(column=1,row=0)

canvas = Canvas(width=400,height=400,bg=BG_COLOR,highlightthickness=0)
img = PhotoImage(file='clock.PNG')
canvas.create_image(200,200,image=img)
timer_txt = canvas.create_text(200,280,text='00:00',fill='black',font=(FONT_NAME,20,'bold'))
canvas.grid(column=1,row=1)

start_btn = Button(width=10,text='Start',highlightthickness=0,command=call_timer)
start_btn.grid(column=0,row=2)

reset_btn = Button(width=10,text='Reset',highlightthickness=0,command=reset_timer)
reset_btn.grid(column=2,row=2)

check_marks = Label(fg='green',bg=BG_COLOR)
check_marks.grid(column=0,row=1)

tela.mainloop()