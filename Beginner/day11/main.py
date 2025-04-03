import random
from art import logo

from art import logo

cartas = {'Ás': 1,'2': 2,'3' : 3, '4' : 4,'5' : 5,'6' : 6,'7' : 7,'8': 8,'9': 9,'10': 10,'11': 10,'12': 10,'13' : 10}

def sorteio(baralho,qtd_de_cartas,state):
    if state == 0: #sorteio inicial
        tempCards = [] #LISTA QUE ARMAZENA AS CARTAS SORTEADAS
        for i in range(0,qtd_de_cartas):
            tempCards.append(random.choice(list(cartas.keys())))

        soma = 0
        for i in tempCards:
            if i == 'Ás':
                if soma <= 10:
                    soma += 11
                else:
                    soma += 1
            else:
                soma += cartas[i]
        mao = {'cartas': tempCards, 'valor': soma}
        return mao
    else: #novo sorteio
        newCard = random.choice(list(cartas.keys()))
        baralho['cartas'] += newCard
        baralho['valor'] += cartas[newCard]
        return baralho

def WinState():
    if computador['valor'] > jogador['valor']:
        print(f'CARTAS MESA: {computador['cartas']} > {jogador['cartas']} CARTAS Jogador')
        print('\nVOCÊ PERDEU')
    elif computador['valor'] == jogador['valor']:
        print(f'CARTAS MESA: {computador['cartas']} = {jogador['cartas']} CARTAS Jogador')
        print('\nEMPATE')
    elif computador['valor'] < jogador['valor']:
        print(f'CARTASMESA: {computador['cartas']} < {jogador['cartas']} CARTAS Jogador')
        print('\nVOCÊ GANHOU')

entry = input('Deseja jogar uma partida de BlackJack?Sim ou Não\n').lower().strip()

if entry not in ['sim','s']:
    print('Ok! Encerrando Jogo.')

else:
    logo()
    print('\niniciando a distruibuição de cartas...')
    jogador = sorteio(cartas,2,0)
    print(f'Suas Cartas: {jogador['cartas']}. Valor das cartas = {jogador['valor']}')
    computador = sorteio(cartas,2,0)
    print(f"Primeira carta da mesa: ['{computador['cartas'][0]}', '?']")

    entry = input('Deseja pegar mais um carta do baralho?Sim ou Não\n').lower().strip()

    if entry not in ['sim', 's']:
        print('Ok! Encerrando Jogo.')
        WinState()
    else:
        print('\n' * 10)
        print('Pegando mais uma carta do baralho...')
        jogador = sorteio(jogador,1,1)

        if jogador['valor'] > 21:
            print('Você Perdeu!')
            print(f'Suas Cartas: {jogador['cartas']}. Valor das cartas = {jogador['valor']}')
            print('ULTRAPASSOU 21!')
        else:
            print('\n'*10)
            print(f'Suas Cartas: {jogador['cartas']}. Valor das cartas = {jogador['valor']}')

            entry = input('Deseja pegar mais um carta do baralho?Sim ou Não\n').lower().strip()

            if entry not in ['sim', 's']:
                print('Ok! Encerrando Jogo.')
                WinState()
            else:
                print('\n' * 10)
                print('Pegando mais uma carta do baralho...')
                jogador = sorteio(jogador, 1, 1)