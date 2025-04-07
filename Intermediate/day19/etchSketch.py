import turtle
from turtle import Turtle,Screen
writer = Turtle()
screen = Screen()

def moveforward():
    writer.forward(10)
def movebackward():
    writer.backward(10)
def rotateleft():
    writer.setheading(writer.heading() + 10)
def rotateright():
    writer.setheading(writer.heading() - 10)

def clear():
    writer.clear()
    writer.penup()
    writer.home()
    writer.pendown()

screen.listen()
screen.onkey(moveforward,'w')
screen.onkey(movebackward,'s')
screen.onkey(rotateleft,'a')
screen.onkey(rotateright,'d')
screen.onkey(clear,'c')

screen.exitonclick()