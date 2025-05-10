import turtle

def create_bullet():
    bullet = turtle.Turtle()
    bullet.shape("circle")
    bullet.color("red")
    bullet.penup()
    bullet.shapesize(stretch_wid=0.5, stretch_len=0.5)
    bullet.hideturtle()
    return bullet

def fire_bullet(bullet, player, state):
    if state == "ready":
        bullet.setposition(player.xcor(), player.ycor() + 10)
        bullet.showturtle()
        return "fire"
    return state
