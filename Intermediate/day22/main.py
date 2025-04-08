from turtle import Screen
from paddle import Paddle
from ball import Ball
from pontos import Scoreboard
import time

tela = Screen()
tela.bgcolor('black')
tela.setup(width=800,height=600)
tela.title('Pong_Game')
tela.tracer(0)

r_paddle = Paddle((350,0))
l_paddle = Paddle((-350,0))
bola = Ball()
placar = Scoreboard()

tela.listen()
tela.onkey(r_paddle.go_up,'Up')
tela.onkey(r_paddle.go_down,'Down')
tela.onkey(l_paddle.go_up,'w')
tela.onkey(l_paddle.go_down,'s')

game_on = True

while game_on:
    time.sleep(bola.movespeed)
    tela.update()
    bola.move()

    if bola.xcor() > 330 and abs(bola.ycor() - r_paddle.ycor()) < 50:
        bola.setx(330)  # impede que ela "atravesse" o paddle
        print('right pong')
        bola.bounce_x()
        bola.movespeed *= 0.9

    elif bola.xcor() < -330 and abs(bola.ycor() - l_paddle.ycor()) < 50:
        bola.setx(-330)
        print('left pong')
        bola.bounce_x()
        bola.movespeed *= 0.9

    if bola.ycor() > 280 or bola.ycor() < -280: #quando acerta o fundo ou o topo da tela
        bola.bounce_y()

    if bola.xcor() > 390:
        bola.reset()
        bola.movespeed = 0.1
        placar.leftside_point()
        time.sleep(1)

    elif bola.xcor() < -390:
        bola.reset()
        bola.movespeed = 0.1
        placar.rightside_point()
        time.sleep(1)
tela.exitonclick()