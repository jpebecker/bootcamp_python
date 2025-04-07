from turtle import Turtle
import random
class Collectable(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.penup()
        self.shapesize(stretch_wid=0.5,stretch_len=0.5)
        self.color('red')
        self.speed('fastest')
        self.refresh()

    def refresh(self):
        rand_X = random.randint(-250,250)
        rand_y = random.randint(-250,250)
        self.goto((rand_X,rand_y))