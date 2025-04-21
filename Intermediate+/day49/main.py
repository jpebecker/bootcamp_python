from selenium import webdriver
import functions as fc
from selenium.webdriver.support.ui import WebDriverWait
###################################################################Entradas Setup
key_words = input('Digite palavras-chave para pesquisar as vagas, separadas por vírgula:\n').lower().strip().split(',')
location = input('Digite a localização para pesquisa:\n').lower().strip()
print(f'Palavras Chaves:{key_words}')
print(f'\nProcurando vagas de {", ".join(key_words)} em {location}.\n')
print("#=============================================================================#")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

browser = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(browser, 10)

browser.get('https://www.linkedin.com/login/pt?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

fc.login(browser, wait, key_words,location) #começa a cadeia de açoes

print("#=============================================================================#")

'''
OBS: A UL QUE O PROGRAMA CAPTURA AO SOLICITAR A PAGINA DAS VAGAS TEM APROXIMADAMENTE 50 LI'S, DESSE MODO 
NAO COGITEI FAZER UM LIMITE SUPERIOR PARA A CONTAGEM DE VAGAS, MAS É BEM SIMPLES
DE ATUALIZAR A UL E FAZER COM BASE NESTE LIMITE, CONSIDERANDO QUE 50 VAGAS É UM BOM NUMERO PARA CHECAR
EU PREFERI DEIXAR O PADRÃO - CASO FAZER MAIOR TEM QUE PROGRAMAR A TROCA DE PAGINAS TAMBÉM
'''