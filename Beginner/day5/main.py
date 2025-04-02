import random

print('Criador de senha automático')

letras = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
numeros = ['0','1','2','3','4','5','6','7','8','9']
simbols = ['!','$','*','@','_']

letters_qtd = int(input('Quantos letras terão em sua senha?\n'))
symbols_qtd = int(input('Quantos símbolos terão em sua senha?\n'))
num_qtd = int(input('Quantos números terão em sua senha?\n'))

password = []

for char in range(0,letters_qtd):
    password.append(random.choice(letras))

for char in range(0,symbols_qtd):
    password.append(random.choice(simbols))

for char in range(0,num_qtd):
    password.append(random.choice(numeros))

random.shuffle(password)
shuffledPassword = ''.join(password)

print(f'Sua senha é: {shuffledPassword}')