def turn_left():
    print('Robo Vira Esquerda')

def at_goal():
    print('verifica se o robo está na posição do objetivo')

def right_is_clear():
    print('verifica se o bloco ao lado direito do robo esta liberado')

def move():
    print('robo anda um bloco na direção que estiver virado')

def front_is_clear():
    print('verifica se a frente do robo não tem obstaculo')

#codigo comeca aqui
turn_left()

def virar_right():
    turn_left()
    turn_left()
    turn_left()
def turn_around():
    turn_left()
    turn_left()

while not at_goal():
    if right_is_clear():
        virar_right()
        move()
    else:
        if front_is_clear():
            virar_right()
            turn_left()
            move()
        else:
            turn_around()
