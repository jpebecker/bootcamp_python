from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

catalogo = Menu()
cafeteira = CoffeeMaker()
caixa = MoneyMachine()

while True:
    print('*'*70)
    entry = input(f'Digite a opção de café que você deseja ({catalogo.get_items()}):\n').strip().lower()
    if entry == 'report':
        cafeteira.report()
        caixa.report()
    elif entry == 'off':
        break
    else:
        if cafeteira.is_resource_sufficient(catalogo.find_drink(entry)):
            if caixa.make_payment(catalogo.find_drink(entry).cost):
                print('preparando seu café...')
                cafeteira.make_coffee(catalogo.find_drink(entry))
            else:
                print('Erro no pagamento')
        else:
            print('Faltam recursos')