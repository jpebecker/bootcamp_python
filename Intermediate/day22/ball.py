from turtle import Turtle

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.color('white')
        self.shape('circle')
        self.penup()
        self.xmove = 10
        self.ymove = 10
        self.movespeed = 0.1

    def move(self):
        new_X = self.xcor() + self.xmove
        new_Y = self.ycor() + self.ymove
        self.goto(new_X,new_Y)

    def bounce_y(self):
        self.ymove *= -1

    def bounce_x(self):
        self.xmove *= -1

    def reset(self):
        self.goto(0,0)
        self.bounce_x()
