import random
from art import logo

cartas = {'Ás': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11': 10, '12': 10,
          '13': 10}

def sorteio(baralho, qtd_de_cartas, state):
    if state == 0:  # Sorteio inicial
        tempCards = []
        soma = 0
        for _ in range(qtd_de_cartas):
            card = random.choice(list(cartas.keys()))
            tempCards.append(card)
            soma += 11 if card == 'Ás' and soma <= 10 else cartas[card] #se puder utiliza o as como 11 e nao 1

        return {'cartas': tempCards, 'valor': soma}

    else:
        newCard = random.choice(list(cartas.keys()))
        baralho['cartas'].append(newCard)

        if newCard == 'Ás':
            if baralho['valor'] + 11 <= 21:
                baralho['valor'] += 11
            else:
                baralho['valor'] += 1
        else:
            baralho['valor'] += cartas[newCard]

        return baralho

def WinState(): #código validador de vitoria
    print(f"CARTAS FINAIS DA MESA: {computador['cartas']} | VALOR: {computador['valor']}")
    print(f"CARTAS FINAIS DO JOGADOR: {jogador['cartas']} | VALOR: {jogador['valor']}")

    if jogador['valor'] > 21:
        print('\nVOCÊ PERDEU! ULTRAPASSOU 21.')
    elif computador['valor'] > 21:
        print('\nVOCÊ GANHOU! A MESA ULTRAPASSOU 21.')
    elif computador['valor'] > jogador['valor']:
        print('\nVOCÊ PERDEU.')
    elif computador['valor'] < jogador['valor']:
        print('\nVOCÊ GANHOU!')
    else:
        print('\nEMPATE!')

entry = input('Deseja jogar uma partida de BlackJack? (Sim/Não)\n').lower().strip()

if entry not in ['sim', 's']:
    print('Ok! Encerrando Jogo.')

else:
    logo()
    print('\nIniciando a distribuição de cartas...')

    jogador = sorteio(cartas, 2, 0)
    computador = sorteio(cartas, 2, 0)

    print(f"Suas Cartas: {jogador['cartas']}. Valor das cartas = {jogador['valor']}")
    print(f"Primeira carta da mesa: [{computador['cartas'][0]}, '?']")

    while jogador['valor'] < 21:
        entry = input('Deseja pegar mais uma carta? (Sim/Não)\n').lower().strip()
        if entry not in ['sim', 's']:
            break

        jogador = sorteio(jogador, 1, 1)
        print(f"Suas Cartas: {jogador['cartas']}. Valor das cartas = {jogador['valor']}")

        if jogador['valor'] > 21:
            print('\nVOCÊ PERDEU! ULTRAPASSOU 21.')
            exit()

    while computador['valor'] < 17:
        computador = sorteio(computador, 1, 1)

    WinState()