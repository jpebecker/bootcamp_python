import random
stages = [
'''
      _______
     |/      |
     |      (_)
     |      \|/
     |       |
     |      / \
     |
    _|___
 ''',
'''
      _______
     |/      |
     |      (_)
     |      \|/
     |       |
     |      
     |
    _|___
 ''',
'''
      _______
     |/      |
     |      (_)
     |      \|/
     |       
     |      
     |
    _|___
''',
'''
      _______
     |/      |
     |      (_)
     |       |
     |       
     |      
     |
    _|___
''',
'''   _______
     |/      |
     |      (_)
     |      
     |       
     |      
     |
    _|___'''
,
'''
      _______
     |/      |
     |      
     |     
     |       
     |      
     |
    _|___
 '''
]

print('''
 _                                             
| |                                            
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __  
| '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                    __/ |                      
                   |___/      
''')
print('                 Jogo da Forca              ')

palavras = ['lapiseira','borracha','caderneta','canetinha','ventilador','lousa','conselheiro','universidade','espelho','compartilhamento','historia']

chosenW = list(random.choice(palavras))
subttle = []
for l in chosenW:
    subttle.append('_')
vidas = 6

while vidas > 0:
    print('+++++++++++++++++++++++++++++++++++++++++++++++++')
    print(stages[vidas-1])
    print(f'VIDAS: {vidas}')
    print(''.join(subttle))
    entry = input('Digite a letra ou a palavra: ').lower()

    if entry == ''.join(chosenW).lower(): #se acertar direto
        print('Você acertou!')
        break
    elif entry not in chosenW: #se errar a letra
        print('Não contem')
        vidas-=1
        if vidas == 0:
            print('Você Perdeu')
    else:
        for i in range(0,chosenW.count(entry)):
            subttle[chosenW.index(entry)] = entry
            chosenW[chosenW.index(entry)] = entry.upper()

        if ''.join(subttle).lower() == ''.join(chosenW).lower():
            print(''.join(subttle).lower())
            print('Você acertou!')
            break