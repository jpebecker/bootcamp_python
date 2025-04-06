import random
from turtle import Turtle,Screen
#######################################
def GenerateRandomColor():
    r = random.randint(0,255)
    b = random.randint(0,255)
    g = random.randint(0,255)
    randomcolor = (r,g,b)
    return randomcolor
#######################################
writer = Turtle()
writer.shape('circle')
writer.pensize(20)
writer.speed('fastest')
screen = Screen()
screen.colormode(255)
writer.color(GenerateRandomColor())
writer.penup()
writer.setpos(-290,-250)
#######################################
for line in range(10):
    writer.setpos(-290, -250 + 60*line)
    for _ in range(11):
        writer.pendown()
        writer.forward(1)
        writer.penup()
        writer.forward(55)
        writer.color(GenerateRandomColor())
screen.exitonclick()
