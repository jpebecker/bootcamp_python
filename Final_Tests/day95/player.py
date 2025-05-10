import turtle

def create_player():
    player = turtle.Turtle()
    player.shape("triangle")
    player.color("white")
    player.penup()
    player.goto(0, -250)
    player.setheading(90)
    return player

def move_left(player, speed):
    x = player.xcor()
    if x > -280:
        player.setx(x - speed)

def move_right(player, speed):
    x = player.xcor()
    if x < 280:
        player.setx(x + speed)
