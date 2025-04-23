from internet_test import InternetTester
from post_X import X,Post
entryD = int(input('Digite o valor de Download contratado com seu provedor em Mbps: ').strip())
entryUp = int(input('Digite o valor de Upload contratado com seu provedor em Mbps: ').strip())

print(f'\nValor esperado de Download: {entryD}Mbps\n'
      f'Valor esperado de Upload:   {entryUp}Mbps\n'
      f'\nIniciando teste...\n')
Rede = InternetTester(entryD,entryUp)

if Rede.Test_Speed():
      print('\nVelocidade de Banda Larga compatível')
      print('finalizando...')
else:
      print('\nVelocidade de Banda Larga incompatível')
      entry = input('Deseja fazer um post no X reclamando ?\n[S - SIM / N - NÃO]\n>>>')
      if entry.lower() in ['s','sim']:
            my_X = X()
            Post(actual=(Rede.download_speed,Rede.upload_speed), expected=(entryD, entryUp),
                 browser=my_X.browser, url=my_X.url)
      else:
            print('finalizando...')