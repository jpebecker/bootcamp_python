from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.hideturtle()
        self.penup()
        self.goto(0,260)
        self.update_score()

    def update_score(self):
        self.write(f'Pontos: {self.score}', align="center", font=('Arial', 20, 'normal'))
    def increase_point(self):
        self.score += 1
        self.clear()
        self.update_score()

    def EndGame(self):
        self.goto(0, 0)
        self.write(f'FIM DE JOGO',align='center',font=('Arial',24,'normal'))