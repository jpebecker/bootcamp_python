from turtle import Turtle
START_POSITION = [(0,0),(-20,0),(-40,0)]
MOVE_DISTANCE = 20
class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        for p in START_POSITION:
            self.add_segment(p)

    def move(self):
        for square in range(len(self.segments) - 1, 0, -1):  # acopla as partes da snake
            new_X = self.segments[square - 1].xcor()
            new_Y = self.segments[square - 1].ycor()
            self.segments[square].goto(new_X, new_Y)
        self.segments[0].forward(MOVE_DISTANCE)

    def add_segment(self,position):
        new_segment = Turtle('square')
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)

    def extend_snake(self):
        self.add_segment(self.segments[-1].position())
###############################################################move functions
    def up(self):
        if self.head.heading() != 270:
            self.segments[0].setheading(90)
    def down(self):
        if self.head.heading() != 90:
            self.segments[0].setheading(270)
    def left(self):
        if self.head.heading() != 0:
            self.segments[0].setheading(180)
    def right(self):
        if self.head.heading() != 180:
            self.segments[0].setheading(0)
##############################################################3