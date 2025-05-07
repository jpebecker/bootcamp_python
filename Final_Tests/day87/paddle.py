from turtle import Turtle

class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=1, stretch_len=5)  #paddle scale
        self.penup()
        self.goto(0, -250)  #initial pos

    def move_left(self):
        new_x = self.xcor() - 30
        if new_x > -360:  #screen limit
            self.goto(new_x, self.ycor())

    def move_right(self):
        new_x = self.xcor() + 30
        if new_x < 360:  #screen limit
            self.goto(new_x, self.ycor())

    def reset_position(self):
        self.goto(0, -250)