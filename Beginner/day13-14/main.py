from data import data_from_accounts
import data
import random

def account_sort(lista_atual, operation):
    if operation == 0:
        a = random.choice(data_from_accounts)
        b = random.choice(data_from_accounts)
        while b['nome'] == a['nome']:
            b = random.choice(data_from_accounts)
        lista_atual.append(a)
        lista_atual.append(b)
        return lista_atual
    elif operation == 1:
        atual = lista_atual[0]  # quem sobrou
        nova = random.choice(data_from_accounts)
        while nova['nome'] == atual['nome']:
            nova = random.choice(data_from_accounts)
        lista_atual.append(nova)
        return lista_atual

def fim_de_jogo(acertos):
    print('\n' * 10)
    data.endgame()
    print("FIM DE JOGO")
    print(f'\nVocê acertou {acertos} vezes')

data.logoTitle()
print('Bem vindo ao Quem é o Maior?')

accounts_list = []
acertos = 0
accounts_list = account_sort(accounts_list, 0)

while True:
    print(f"\nComparando entre A: {accounts_list[0]['nome']}, {accounts_list[0]['description']} do {accounts_list[0]['country']}")
    data.logoVS()
    print(f"e B: {accounts_list[1]['nome']}, {accounts_list[1]['description']} do {accounts_list[1]['country']}")

    entry = input('Quem tem mais seguidores no Instagram?\n').lower().strip()

    if entry == 'a':
        if accounts_list[0]['followers'] > accounts_list[1]['followers']:
            acertos += 1
            accounts_list.remove(accounts_list[0])
            print('Acertasse!')
            accounts_list = account_sort(accounts_list, 1)
        else:
            fim_de_jogo(acertos)
            break
    elif entry == 'b':
        if accounts_list[1]['followers'] > accounts_list[0]['followers']:
            acertos += 1
            accounts_list.remove(accounts_list[1])
            print('Acertasse!')
            accounts_list = account_sort(accounts_list, 1)
        else:
            fim_de_jogo(acertos)
            break