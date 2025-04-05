from catalogo import MENU
from catalogo import art

def preparar_cafe(option,supplies):
    print(f'Preparando seu {option.capitalize()}...')
    art()
    for supply in supplies['ingredientes']:
        if supplies['ingredientes'][supply] < MENU[option]['ingredientes'][supply]:
            print('ERRO: SUPRIMENTOS INSUFICIENTES, CONSULTAR ASSISTÊNCIA')
            print(f'DEVOLVENDO SEU TROCO: R${MENU[option]["preco"]}')
            supplies['dinheiro'] -= MENU[option]['preco']
            return supplies
        else:
            supplies['ingredientes'][supply] -= MENU[option]['ingredientes'][supply]
    return supplies

def cobrar_cafe(option,supplies):
    print(f'Pague pelo seu {option.capitalize()}...')
    price = MENU[option]['preco']
    moedas = {'5 centavos' : 0.05, '10 centavos' : 0.1, '25 centavos' : 0.25, '50 centavos' : 0.5, '1 real' : 1}
    print(f'PREÇO: R${price}')
    valor = 0
    for item in moedas:
        valor += int(input(f'Quantas moedas de {item} você insere?\n'))*moedas[item]
    if round(valor,2) == round(price,2): #arredondado pois houve erro de entrada por causa da multiplicacao
        supplies['dinheiro'] += round(valor,2)
        return True and supplies
    elif round(valor,2) > round(price,2):
        supplies['dinheiro'] += price
        print(f'Seu troco deu R${valor-price}')
        return True and supplies
    else:
        print('Dinheiro insuficiente')
        return False
suprimentos = {'ingredientes' : {'agua' : 1000 , 'leite' : 500 , 'cafe' : 300},'dinheiro': 0}
while True:
    print('*'*60)
    entry = input('Digite o que você deseja (americano,latte,cappuccino):\n').lower().strip()

    if entry == 'americano':
        if cobrar_cafe(option='americano',supplies=suprimentos):
            suprimentos = preparar_cafe(option='americano',supplies=suprimentos)
        else:
            print('ERRO: HOUVE UM ERRO NA COBRANÇA')
    elif entry == 'latte':
        if cobrar_cafe(option='latte',supplies=suprimentos):
            suprimentos = preparar_cafe(option='latte',supplies=suprimentos)
        else:
            print('ERRO: HOUVE UM ERRO NA COBRANÇA')
    elif entry == 'cappuccino':
        if cobrar_cafe(option='cappuccino',supplies=suprimentos):
            suprimentos = preparar_cafe(option='cappuccino',supplies=suprimentos)
        else:
            print('ERRO: HOUVE UM ERRO NA COBRANÇA')
    elif entry == 'off':
        print('desligando máquina...')
        print('\n*'*10)
        break
    elif entry == 'report':
        print('imprimindo informações de suprimento...')
        for item, valor in suprimentos['ingredientes'].items():
            unidade = 'ml' if item != 'cafe' else 'gr'
            print(f'{item.capitalize()}: {valor}{unidade}')
        print(f'Dinheiro: R${suprimentos["dinheiro"]:.2f}')
    else:
        print('ERRO: Comando não reconhecido')