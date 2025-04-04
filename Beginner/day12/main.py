import random
from art import logo
logo()
print('Bem vindo ao jogo de adivinhar números')
print('\nComputador: Eu estou pensando em um número entre 1 e 100...\n')
num = random.randint(1,100)
dif = input('Escolha uma dificuldade (Tranquila / Moderada):\n').lower().strip()

if dif == 'tranquila':
    chances = 8
elif dif == 'moderada':
    chances = 5
elif dif == 'impossivel':
    chances = 3
else:
    print('ERRO: Comando não reconhecido')
    chances = 0

print('\n'*10)

while chances!=0:
    print(f'Você tem {chances} chances para acertar...\n')

    entry = int(input('Digite um número: '))

    if entry == num:
        print("VOCÊ ACERTOU!")
        print(f'O número era {num}')
        break
    elif entry > num:
        print('Mais baixo...')
        chances -=1
    elif entry < num:
        print('Mais alto...')
        chances -=1
if chances == 0:
    print(f'Perdeste! O número era {num}')