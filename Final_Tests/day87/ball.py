from turtle import Turtle

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(0, -230)  #pos above paddle
        self.x_move = 3
        self.y_move = 3
        self.move_speed = 0.01  #speed = difficulty?

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_x(self): #invert x axis
        self.x_move *= -1

    def bounce_y(self): #inverte y axis
        self.y_move *= -1

    def reset_position(self): #restart pos
        self.goto(0, -230)
        self.bounce_y()
