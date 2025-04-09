import random
import time
from turtle import Turtle
COLORS = ['blue','yellow','red','black','green','orange','purple']
STARTING_X = 305
MOVESPEED = 0.5
MOVE_INCREMENT = 10
CARS = []
class CarManager(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape('square')
        self.shapesize(stretch_wid=2, stretch_len=1)
        self.setheading(90)
        self.color(random.choice(COLORS))
        new_Y = random.randint(-250, 250)
        self.goto(STARTING_X, new_Y)
        self.moveincrement = MOVE_INCREMENT
    def moveacross(self):
        new_X = self.xcor() - MOVESPEED * self.moveincrement
        self.goto(new_X, self.ycor())

    def newlevel(self):
        self.moveincrement += 1
