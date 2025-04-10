from turtle import Turtle

FONT = ('Courier',10,'bold')
class State(Turtle):
    def __init__(self,title,position):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.goto(position)
        self.write(title, align='center', font=FONT)
        self.name = title
