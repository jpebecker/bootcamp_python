import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

print('crossing game')
tela = Screen()
tela.setup(width=600,height=600)
tela.tracer(0)
tela.listen()
player = Player()
placar = Scoreboard()

cars = []

tela.onkey(player.moveup,'Up')
tela.onkey(player.moveup,'w')
gameturn = 0
game_on = True

while game_on:
    time.sleep(0.1)
    if gameturn == 8:
        newcar = CarManager()
        cars.append(newcar)
        gameturn = 0

    tela.update()
    gameturn += 1

    if player.ycor() >= player.finish_line_y:
        print('chegou ao fim')
        placar.newlevel()
        time.sleep(1)
        player.newlevel()
        for car in cars:
            car.newlevel()

    for car in cars:
        car.moveacross()
        if car.xcor() < -320: #verifica se o carro esta fora da tela e exclui ele do programa
            car.hideturtle()
            car.clear()
            cars.remove(car)
            del car
        else:
            if player.distance(car) < 30:
                print('contato')
                placar.gameover()
                game_on = False

tela.exitonclick()