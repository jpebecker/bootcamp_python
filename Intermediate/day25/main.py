import pandas,turtle
from states_spawn import State
###############################
transformedData = []
with open('estados_brasil.csv',mode='r',encoding='utf-8') as data:
    transformedData = pandas.read_csv(data)
####################################################
#print(transformedData['estado'].tolist())
tela = turtle.Screen()
tela.title('Brasil Guess the State')
tela.setup(width=750,height=750)
img = 'brasil_map.gif'
tela.addshape(img)
turtle.shape(img)
states_spawneds = []
#############################################################
entry_state = tela.textinput(title='Estados do Brasil',prompt='Digite um estado do Brasil...').title()

while len(states_spawneds)<27:
    if entry_state in transformedData['estado'].tolist() and entry_state not in states_spawneds:
        estado = transformedData.loc[transformedData['estado'] == entry_state].iloc[0]
        newState = State(entry_state, (estado['x'], estado['y']))
        states_spawneds.append(entry_state)
        if len(states_spawneds) != 27:
            entry_state = tela.textinput(title=f'{len(states_spawneds)}/27 estados do Brasil',
                                     prompt='Digite um estado do Brasil...').title()
    elif entry_state in states_spawneds:
        entry_state = tela.textinput(title='Já digitou este Estado',
                                     prompt='Digite um estado do Brasil...').title()
    elif entry_state.lower() == 'exit':
        break
    else:
        entry_state = tela.textinput(title='Estado incorreto',
                                     prompt='Digite um estado do Brasil...').title()
############################################################################################
Final_Text = turtle.Turtle()
Final_Text.hideturtle()
Final_Text.penup()
Final_Text.goto(0, 0)
Final_Text.write('FIM DE JOGO',align='center',font=('Arial',20,'bold'))
tela.exitonclick()
#########################################################################################