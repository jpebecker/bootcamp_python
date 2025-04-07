import random
from turtle import Turtle,Screen
colors = {'vermelho':'red','roxo':'purple','verde':'green','amarelo':'yellow','azul':'blue','laranja':'orange'}
colorsLIST = ['red','purple','green','yellow','blue','orange']
screen = Screen()
screen.setup(500,400)
turtles = []
init_race = False

for i in range(0,len(colors)):
    turtles.append(Turtle(shape='turtle'))
    turtles[i].color(colorsLIST[i])
    turtles[i].penup()
    turtles[i].goto((-230,-105 + 40*i)) #leva pra posicao inicial

choice = screen.textinput('Quem vencerá a corrida?','Digite uma cor:').strip().lower()

if choice:
    init_race = True

while init_race:

    for turtle in  turtles:

        if turtle.xcor() > 230:
            if colors[choice] == turtle.pencolor():
                print('VOCÊ GANHOU A CORRIDA')
                break
            else:
                print(f'VOCÊ PERDEU A CORRIDA.{next((k for k, value in colors.items() if value == turtle.pencolor()), None).capitalize()} GANHOU')
                init_race = False
                break

        random_distance = random.randint(5,10)
        turtle.forward(random_distance)

screen.exitonclick()

