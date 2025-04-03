print('''
 _____________________
|  _________________  |
| | Python       0. | |
| |_________________| |
|  ___ ___ ___   ___  |
| | 7 | 8 | 9 | | + | |
| |___|___|___| |___| |
| | 4 | 5 | 6 | | - | |
| |___|___|___| |___| |
| | 1 | 2 | 3 | | x | |
| |___|___|___| |___| |
| | . | 0 | = | | / | |
| |___|___|___| |___| |
|_____________________|
'''
)
def Calc_func(number1,number2,to_do):
    """Calcula uma operação entre dois números"""
    if to_do == '+':
        print(f'Resultado: {number1}{to_do}{number2} = {number1 + number2}')
        return number1 + number2
    elif to_do == '-':
        print(f'Resultado: {number1}{to_do}{number2} = {number1 - number2}')
        return number1 - number2
    elif to_do == '/':
        print(f'Resultado: {number1}{to_do}{number2} = {number1 / number2}')
        return number1 / number2
    elif to_do == '*':
        print(f'Resultado: {number1}{to_do}{number2} = {number1 * number2}')
        return number1 * number2
    else:
        print('ERRO: Operador não Reconhecido')
        return

print('Bem vindo a Calculadora')

num1 = float(input('\nDigite um primeiro número: '))
task = input('\nDigite um Operador [+ - / *]: ').strip()
num2 = float(input('\nDigite um segundo número: '))
print('\nCalculando...')
actualNum = Calc_func(num1,num2,task)

while True:
    print('\n'*10)
    entry = input(f'Deseja Continuar com {actualNum}? Sim ou Não\n').lower().strip()
    if entry not in ['sim','s']:
        num1 = float(input('\nDigite um primeiro número: '))
        task = input('\nDigite um Operador [+ - / *]: ').strip()
        num2 = float(input('\nDigite um segundo número: '))
        print('\nCalculando...')
        actualNum = Calc_func(num1, num2, task)
    elif entry in ['sim','s']:
        task = input('\nDigite um Operador [+ - / *]: ').strip()
        num2 = float(input('\nDigite um segundo número: '))
        print('\nCalculando...')
        actualNum = Calc_func(actualNum, num2, task)
    else:
        print('Comando não reconhecido...')
        print('Encerrando...')