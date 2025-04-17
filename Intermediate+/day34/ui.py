from tkinter import *
from tkinter import messagebox
from quiz_brain import QuizBrain
FONT = ('Arial', 14, 'bold')
class QuizUI:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.tela = Tk()
        self.tela.title('Car Quiz')
        self.themeColor = '#6F826A'
        self.tela.config(padx=20,pady=20,bg=self.themeColor)
        self.canvas = Canvas(width=300,height=300)
        self.question_text = self.canvas.create_text(150,100,text='Question Text',fill=self.themeColor,
                                                     font=('Courier',16,'italic'),
                                                     width=250)

        self.score_label = Label(text='Score=0', fg='white',bg=self.themeColor,font=FONT)
        self.score_label.grid(column=1,row=0,sticky='e')

        true_image = PhotoImage(file='images/true.png')
        false_image = PhotoImage(file='images/false.png')

        self.rightBtn = Button(image=true_image, highlightthickness=0, borderwidth=0, command=self.right_answer)
        self.rightBtn.grid(column=0,row=2,sticky='w')
        self.WrongBtn = Button(image=false_image, highlightthickness=0, borderwidth=0, command=self.wrong_answer)
        self.WrongBtn.grid(column=1, row=2,sticky='e')

        self.canvas.grid(column=0, row=1, columnspan=2,pady=20)

        self.new_question()

        self.tela.mainloop()

    def right_answer(self):
        self.disable_buttons()
        self.feedback_question(self.quiz.check_answer('True'))

    def wrong_answer(self):
        self.disable_buttons()
        self.feedback_question(self.quiz.check_answer('False'))

    def feedback_question(self, is_right: bool):
        if is_right:
            self.canvas.config(bg='green')
            self.canvas.itemconfig(self.question_text, fill='black')
        else:
            self.canvas.config(bg='red')
            self.canvas.itemconfig(self.question_text, fill='black')
        self.tela.after(1000, self.new_question)

    def disable_buttons(self):
        self.rightBtn.config(state='disabled')
        self.WrongBtn.config(state='disabled')

    def enable_buttons(self):
        self.rightBtn.config(state='normal')
        self.WrongBtn.config(state='normal')

    def new_question(self):
        self.canvas.config(bg='white')
        if self.quiz.still_has_questions and self.quiz.question_number != 10:
            self.enable_buttons()
            self.canvas.itemconfig(self.question_text, fill=self.themeColor)
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
            self.score_label.config(text=f'Score:{self.quiz.score}')
        else:
            self.canvas.itemconfig(self.question_text, text='FIM DE JOGO', fill=self.themeColor)
            messagebox.showinfo(title='FIM de JOGO', message="You've completed the quiz!\n\n"
                                                             f"Your score was {self.quiz.score}/"
                                                             f"{len(self.quiz.question_list)}")
            self.rightBtn.config(state='disabled')
            self.WrongBtn.config(state='disabled')
            self.tela.quit()
