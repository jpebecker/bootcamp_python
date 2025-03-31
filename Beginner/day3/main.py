print('''
 _______________________________________________________________________
|       (_      (_      (_      (_      (_      (_      (_      (_      |
|        _)      _)      _)      _)      _)      _)      _)      _)     |
|  _   _(  _   _(  _   _(  _   _(  _   _(  _   _(  _   _(  _   _(  _   _|
|_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |
|      _)      _)      _)      _)      _)      _)      _)      _)       |
|     (_      (_      (_      (_      (_      (_      (_      (_        |
|_   _  )_   _  )_   _  )_   _  )_   _  )_   _  )_   _  )_   _  )_   _  |
| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_|
|       (_      (_      (_      (_      (_      (_      (_      (_      |
|        _)      _)      _)      _)      _)      _)      _)      _)     |
|  _   _(  _   _(  _   _(  _   _(  _   _(  _   _(  _   _(  _   _(  _   _|
|_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |
|      _)      _)      _)      _)      _)      _)      _)      _)       |
|     (_      (_      (_      (_      (_      (_      (_      (_        |
|_   _  )_   _  )_   _  )_   _  )_   _  )_   _  )_   _  )_   _  )_   _  |
| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_|
|       (_      (_      (_      (_      (_      (_      (_      (_      |
|        _)      _)      _)      _)      _)      _)      _)      _)     |
|_______(_______(_______(_______(_______(_______(_______(_______(_______|
''')
print('                          THE LABIRINT QUEST                         ')

print('bem vindo ao labirinto')
print('\nsua missão é encontrar a saída')
print('só existe um caminho para isto, boa sorte!')

print('\nVocê acorda em uma sala redonda, com uma mesa no centro. Você olha para a porta entreaberta')
entry = input('Você deseja ir até a porta? Sim ou Não\n')

if entry.lower() == 'não':
    print('Você esperou demais e alguém trancou a porta. Você apodreceu naquela sala')
    print('/n Fim de Jogo.')
else:
    print('Você sai pela porta e vê uma pessoa armadurada se aproximando...')
    entry = input('Você espera para conversar com ela? Sim ou Não\n')

    if entry.lower() == 'sim':
        print('Você esperou e foi recapturado. Seu instinto de sobrevivência foi mais fraco')
        print('/nFim de Jogo.')
    else:
        print('Você corre na direção oposta')
        print('\nChegando a um cruzamento de corredores, você precisa decidir...')
        entry = input('Você vira pra direita ou pra esquerda?\n')

        if entry.lower() == 'direita':
            print('Você segue para um salão repleto de guardas e é capturado. Que azar!')
            print('/nFim de Jogo.')
        else:
            print('Você segue para um grande salão vazio. Nele você percebe uma claridade vindo de uma porta.')
            entry = input('Você vai até a porta? Sim ou Não\n')

            if entry.lower() == 'sim':
                print('Você abre a porta e do outro lado está a forja repleta de soldados. Você é pego.')
                print('/nFim de Jogo.')
            else:
                print('Você ignora a porta e vai até o fundo do salão onde vê uma grande pintura')
                entry = input('Você mexe na pintura? Sim ou Não\n')

                if entry.lower() == 'não':
                    print('Você não faz nada e logo é capturado por não conseguir encontrar a saída')
                    print('/nFim de Jogo.')
                else:
                    print('Você arranca a pintura e descobre uma passagem secreta atrás dela. É sua rota de fuga')
                    print('Conseguiste escapar. Fim de jogo')
