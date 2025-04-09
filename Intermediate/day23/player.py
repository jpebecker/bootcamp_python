from turtle import Turtle
STARTING_POS = (0,-280)
MOVESPEED = 10
FINISH_LINE_Y = 285

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('turtle')
        self.penup()
        self.color('green')
        self.goto(STARTING_POS)
        self.setheading(90)
        self.finish_line_y = FINISH_LINE_Y

    def moveup(self):
        new_y = self.ycor() + MOVESPEED
        self.goto(self.xcor(), new_y)

    def newlevel(self):
        self.goto(STARTING_POS)