from turtle import Screen
from snake import Snake
from score import Scoreboard
from collectable import Collectable
import time

screen = Screen()
screen.tracer(0)
screen.bgcolor('green')
screen.setup(width=600,height=600)
screen.title('Jogo da Cobrinha')
game_on = True

snake = Snake()
food = Collectable()
placar = Scoreboard()

screen.listen()
screen.onkey(snake.up,'w')
screen.onkey(snake.down,'s')
screen.onkey(snake.left,'a')
screen.onkey(snake.right,'d')

while game_on:
    screen.update()
    time.sleep(0.1) #velocidade
    snake.move()

    if snake.head.distance(food) < 15:
        print('food collected')
        food.refresh()
        placar.increase_point()
        snake.extend_snake()

    if snake.head.xcor() > 280 or snake.head.xcor() <-280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
        print('Ultrapassou a tela')
        placar.EndGame()
        game_on = False

    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            print('colidiu com corpo')
            placar.EndGame()
            game_on = False

screen.exitonclick()