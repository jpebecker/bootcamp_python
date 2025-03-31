print('Bem vindo ao calculador de gorjetas!')
value = float(input("Digite o valor da conta em reais: R$"))

tip = int(input('Qual a porcentagem de gorjeta sob a conta que você deseja pagar?\n'))

pessoas = int(input("Quantas pessoas irão pagar a conta?\n"))

gorjeta = (value/100) * tip

value += gorjeta

print(f'\nCada um deverá pagar: R${round(value/pessoas,2)}')
