import time
from turtle import Turtle

FONT = ("Arial", 18, 'bold')

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.level = 1
        self.goto(-250,270)
        self.refreshscore()

    def refreshscore(self):
        self.clear()
        self.write(f'Level {self.level}',align='center',font=FONT)

    def newlevel(self):
        self.level += 1
        self.refreshscore()

    def gameover(self):
        self.home()
        self.write(f'GAME OVER', align='center', font=FONT)