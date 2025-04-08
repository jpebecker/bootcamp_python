from turtle import Turtle
class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color('white')
        self.penup()
        self.hideturtle()
        self.left_score = 0
        self.right_score = 0
        self.updatescoreboard()

    def updatescoreboard(self):
        self.clear()
        self.goto(-80,200)
        self.write(self.left_score,align='center',font=('Courier',70,'normal'))
        self.goto(80,200)
        self.write(self.right_score,align='center',font=('Courier',70,'normal'))

    def leftside_point(self):
        self.left_score += 1
        self.updatescoreboard()

    def rightside_point(self):
        self.right_score += 1
        self.updatescoreboard()
