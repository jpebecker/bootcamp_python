from turtle import Turtle

class GameManager(Turtle):
    def __init__(self):
        super().__init__()
        #configs
        self.score = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(-380, 260) #position
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f"Points: {self.score}", align="left", font=("Arial", 16, "bold"))

    def add_score(self):
        self.score += 1
        self.update_score()

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=("Arial", 24, "bold"))

    def victory(self):
        self.goto(0, 0)
        self.write("You Win!", align="center", font=("Courier", 24, "bold"))
