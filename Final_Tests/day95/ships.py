import turtle
import random

class Enemy:
    def __init__(self):
        self.body = turtle.Turtle()
        self.body.shape("circle")
        self.body.color("green")
        self.body.penup()
        self.body.goto(random.randint(-250, 250), random.randint(300, 600))  #outside screen
        self.speed = random.uniform(0.3, 0.6)  # random speed

    def move(self):
        y = self.body.ycor()
        self.body.sety(y - self.speed)

    def is_off_screen(self):
        return self.body.ycor() < -290  #passed the player

    def reset_position(self):
        self.body.goto(random.randint(-250, 250), random.randint(300, 600))
