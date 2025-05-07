import time
from turtle import Screen, Turtle
from paddle import Paddle
from ball import Ball
from bricks import Brick
from game_manager import GameManager


class GameInterface:
    def __init__(self):
        #screen config
        self.screen = Screen()
        self.screen.title("Breakout Clone")
        self.screen.bgcolor("black")
        self.screen.setup(width=800, height=600)
        self.screen.tracer(0)

        # Game objects (outras classes)
        self.paddle = Paddle()
        self.ball = Ball()
        self.score = GameManager()
        self.bricks = []

        #delay of hits
        self.last_hit_time = 0  #last hit time
        self.hit_delay = 0.08 #hit delay

        self.create_bricks()
        self.get_controls()

        #game state
        self.running = True

    def create_bricks(self):  # Cria a disposição dos blocos
        colors = ["red", "orange", "green", "yellow"]
        rows = 4
        columns = 10
        x_start = -350  # Posição x
        y_start = 250  # Posição y
        for row in range(rows):
            for col in range(columns):
                x = x_start + col * 75
                y = y_start - row * 30
                brick = Brick(x, y, colors[row % len(colors)])
                self.bricks.append(brick)

    def get_controls(self):
        self.screen.listen()
        self.screen.onkeypress(self.paddle.move_left, "Left")
        self.screen.onkeypress(self.paddle.move_right, "Right")

    def show_restart_btn(self):
        button = Turtle()
        button.hideturtle()
        button.penup()
        button.goto(-80, -50)
        button.color("white", "red")
        button.begin_fill()
        for _ in range(2):
            button.forward(160)
            button.right(90)
            button.forward(40)
            button.right(90)
        button.end_fill()

        button.goto(0, -70)
        button.color("black")
        button.write("Play Again", align="center", font=("Arial", 14, "bold"))

        return (-80, -50, 80, -90)  #btn pos

    def on_click(self, x, y, x1, y1, x2, y2):
        if x1 < x < x2 and y2 < y < y1:
            self.screen.clearscreen()
            self.__init__()  # restart the class
            self.run()  # restart the game method

    def run(self):
        while self.running:
            self.screen.update()
            time.sleep(0.01)
            self.ball.move()

            #lateral wall colision
            if self.ball.xcor() > 390 or self.ball.xcor() < -390:
                self.ball.bounce_x()

            #up wall colision
            if self.ball.ycor() > 290:
                self.ball.bounce_y()

            #paddle colision
            if self.ball.distance(self.paddle) < 50 and self.ball.ycor() < -240:
                self.ball.bounce_y()

            #brick colision
            for brick in self.bricks[:]:
                if self.ball.distance(brick) < 35:  #distance of colision detection
                    current_time = time.time()
                    if current_time - self.last_hit_time >= self.hit_delay:
                        # Se a bola vem de cima, aplica o bounce_y
                        if self.ball.ycor() > brick.ycor():  #ball coming upwards the brick
                            self.ball.bounce_y()
                        elif self.ball.ycor() < brick.ycor():  #ball coming from under the brick
                            self.ball.bounce_y()
                            self.ball.bounce_x()
                        else:
                            self.ball.bounce_x() #ball coming sideways

                        #last hit time
                        self.last_hit_time = current_time

                        #block hit
                        destroyed = brick.hit()
                        if destroyed:
                            self.bricks.remove(brick)
                            self.score.add_score()

            #lose state
            if self.ball.ycor() < -280:  #passed the paddle
                self.score.game_over()
                self.running = False
                x1, y1, x2, y2 = self.show_restart_btn()
                self.screen.onclick(lambda x, y: self.on_click(x, y, x1, y1, x2, y2))

            #win state
            if not self.bricks:
                self.score.victory()
                self.running = False
                x1, y1, x2, y2 = self.show_restart_btn()
                self.screen.onclick(lambda x, y: self.on_click(x, y, x1, y1, x2, y2))

        #open screen fixed
        self.screen.mainloop()