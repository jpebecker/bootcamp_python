print('**********************Controlador de Leilão Virtual*********************')

lances = {}
maior_lance = ['',0]
while True:
    print('--------------------------------------------------------')
    entry = input('\nDeseja computar um lance? Sim ou Não\n').lower().strip()
    if entry not in ['sim','s']:
        print('Encerrando audição...\n')
        break
    else:
        user = input('Digite a identificação/nome do lance\n').capitalize().strip()
        valor = float(input('Digite o lance, em reais: R$'))

        lances.update({user:valor})

for lance in lances:
    if lances[lance] > maior_lance[1]:
        maior_lance[0] = lance
        maior_lance[1] = lances[lance]

print(f'O maior lance foi de {maior_lance[0]} com R${maior_lance[1]}')