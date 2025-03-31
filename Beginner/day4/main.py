from random import randint

print("Bem vindo ao pedra - papel - tesoura")

entry = int(input('\nDigite 0 para pedra, 1 para papel, 2 para tesoura:\n'))
bot = randint(0,2)
pedra = ('''
                _      ___ __
                |  _,-' _ `\__)
                |~'    ' `\()
                |       (____)
                |      (_____)
                |--.____(___)
        ''')
tesoura = ('''
                            .-.  _
                            | | / )
                            | |/ /
                           _|__ /_
                          / __)-' )
                          \  `(.-')
                           > ._>-'
                          / \/

        ''')
papel = ('''
                     _.-._
                    | | | |_
                    | | | | |
                    | | | | |
                  _ |  '-._ |
                  \`\`-.'-._;
                   \    '   |
                    \  .`  /
                     |    |
        ''')
images_ascii = [pedra,papel,tesoura]

if entry == bot:
    print('Escolha do Usuário:')
    print(images_ascii[entry])
    print('Escolha do Computador:')
    print(images_ascii[bot])
    print('EMPATE')
elif entry == 0:
    print('Escolha do Usuário:')
    print(images_ascii[entry])
    if bot == 1:
        print('Escolha do Computador:')
        print(images_ascii[bot])
        print('PERDESTE')
    else:
        print('Escolha do Computador:')
        print(images_ascii[bot])
        print('GANHASTE')
elif entry == 1:
    print('Escolha do Usuário:')
    print(images_ascii[entry])
    if bot == 2:
        print('Escolha do Computador:')
        print(images_ascii[bot])
        print('PERDESTE')
    else:
        print('Escolha do Computador:')
        print(images_ascii[bot])
        print('GANHASTE')
elif entry == 2:
    print('Escolha do Usuário:')
    print(images_ascii[entry])
    if bot == 0:
        print('Escolha do Computador:')
        print(images_ascii[bot])
        print('PERDESTE')
    else:
        print('Escolha do Computador:')
        print(images_ascii[bot])
        print('GANHASTE')
