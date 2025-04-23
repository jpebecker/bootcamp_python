from api_bridge import *

L_entry = input('Digite uma Cidade para buscar por eventos: ').strip().title()
eventos = buscar_eventos(local=L_entry)
print('Recuperando resultados:')
for evento in eventos:
    print('='*150)
    for key,value in evento.items():
        print(f'{key}:{value}')
print('='*150)
print('fim de consulta')