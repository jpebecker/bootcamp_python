def cifrar(message,shifts,command):
    newMessage = ""
    if command == 'decode':
        shifts *= -1
    for letter in message:
        if letter not in alfabeto:
            newMessage += letter
        else:
            newPosition = alfabeto.index(letter) + shifts
            newPosition %= len(alfabeto)  # cicla o alfabeto
            newMessage += alfabeto[newPosition]
    return newMessage

alfabeto =  [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z'
]

while True:
    order = input("Digite 'encode' para encriptar ou 'decode' para descriptar\n").lower().strip()
    if order != 'encode' and order != 'decode':
        print('\nComando não reconhecido...Encerrando')
        break
    else:
        mensagem = input('Digite o texto para processamento: ').lower()
        turno = int(input('Digite o número de ciclos da cifra: '))

        if order == 'encode':
            print('\nencriptando mensagem...')
            print()
            print(f'Sua mensagem encriptada é: {cifrar(message=mensagem,shifts=turno,command='encode')}')

        elif order == 'decode':
            print('\ndecriptando mensagem...')
            print()
            print(f'Sua mensagem descriptada é: {cifrar(message=mensagem,shifts=turno,command='decode')}')