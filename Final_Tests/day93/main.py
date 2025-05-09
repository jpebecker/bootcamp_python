from scrape_gov import scrape_inpi
#web scrapping de patentes registradas
print('Coletor de Patentes - WebScrapper')
print('=-'*15)
print('[1] - Marca')
print('[2] - Patente')
print('[3] - Desenho Industrial')
print('[4] - Programa de Computador')
print('=-'*15)

cat_entry = int(input('Digite a categoria de pesquisa: '))
search_entry = input('Digite o termo de consulta (presente no título):\n').lower().strip()

results = scrape_inpi(method=cat_entry,search=search_entry)

if results: #if the list has any returned results
    print(f'Imprimindo resultados sobre {search_entry}\n')
    print('-='*35)
    for item in results:
        print(f'MARCA: {item['marca']} // TITULAR: {item['titular']}\n SITUAÇÃO: {item['situation']}\n DATA: {item['data']}')
else:
    print(f'Não se teve resultados para {search_entry} no INPI pela categoria selecionada.')