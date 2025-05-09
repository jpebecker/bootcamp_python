from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpCond
#brownser options below
options = Options()
options.add_argument('--headless') #no visible window
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080') #keep a guaranteed resolution


browser = webdriver.Chrome(options=options) #init the browser
base_url = 'https://busca.inpi.gov.br/pePI/servlet/LoginController?action=login' #base url for a private(non-logged) search at INPI

def scrape_inpi(method, search):
    print('Acessando base do INPI...')
    browser.get(base_url) #acess the page
    try:
        WebDriverWait(browser, 10).until(
            ExpCond.presence_of_element_located((By.XPATH, '//*[@id="Map3"]/area[1]')) #try to get the layout map of btns
        )
    except:
        print('Erro ao carregar o layout do INPI.')
        return

    if method == 1: #brands
        print(f'scraping Marcas registradas no INPI...')
        browser.find_element(By.XPATH, '//*[@id="Map3"]/area[1]').click() #click in the brand btn at homepage
        WebDriverWait(browser,10).until(ExpCond.presence_of_element_located((By.XPATH, '//*[@id="principal"]/table[2]/tbody/tr[1]/td/font/a[1]')))
        browser.find_element(By.XPATH, '//*[@id="principal"]/table[2]/tbody/tr[1]/td/font/a[1]').click() #click at simple search for brands
        WebDriverWait(browser, 10).until(ExpCond.presence_of_element_located((By.NAME, 'marca'))) #wait the entry
        entry_marca = browser.find_element(By.NAME, 'marca')  #get the entry
        entry_marca.send_keys(search) #input the search
        entry_marca.send_keys(Keys.ENTER) #send the search
        r_list = get_results() #call get results
    elif method == 2: #patents and all below are the same route
        print(f'scraping Patentes registradas no INPI...')
        browser.find_element(By.XPATH, '//*[@id="Map3"]/area[5]').click() #click on the method btn
        WebDriverWait(browser, 10).until(ExpCond.presence_of_element_located((By.NAME, 'ExpressaoPesquisa')))
        entry_patente = browser.find_element(By.NAME, 'ExpressaoPesquisa') #get the entry
        entry_patente.click() #select the entry
        entry_patente.send_keys(search) #input the search
        entry_patente.send_keys(Keys.ENTER) #send the search
        r_list = get_results() #call get results
    elif method == 3: #industrial drawings
        print(f'scraping Desenhos Industriais registrados no INPI...')
        browser.find_element(By.XPATH, '//*[@id="Map3"]/area[2]').click()
        WebDriverWait(browser, 10).until(ExpCond.presence_of_element_located((By.NAME, 'ExpressaoPesquisa')))
        entry_patente = browser.find_element(By.NAME, 'ExpressaoPesquisa')
        entry_patente.click()
        entry_patente.send_keys(search)
        entry_patente.send_keys(Keys.ENTER)
        r_list = get_results()
    elif method == 4: #desktop programs
        print(f'scraping Programas de Computador registrados no INPI...')
        browser.find_element(By.XPATH, '//*[@id="Map3"]/area[3]').click()
        WebDriverWait(browser, 10).until(ExpCond.presence_of_element_located((By.NAME, 'ExpressaoPesquisa')))
        entry_patente = browser.find_element(By.NAME, 'ExpressaoPesquisa')
        entry_patente.click()
        entry_patente.send_keys(search)
        entry_patente.send_keys(Keys.ENTER)
        r_list = get_results()
    else: #if the category number is invalid return none
        print('método não registrado para consulta. Retornando...')
        return None

    return r_list #return the results list after get_results

def get_results():
    try: #try getting the table at the result page
        WebDriverWait(browser, 10).until(
            ExpCond.presence_of_element_located((By.XPATH, '//*[@id="principal"]/table[3]'))
        )
        table = browser.find_element(By.XPATH, '//*[@id="principal"]/table[3]') #get table
        table_lines = table.find_elements(By.XPATH, './/tr[@class="normal"]')#get table lines

        formatted_results = []
        for item in table_lines: #loop through table lines searching for...
            try:
                cols = item.find_elements(By.TAG_NAME, 'td') #columns of result in each line
                if len(cols) >= 5: #if the length is enough to get the situation
                    situation = cols[5].text.strip() #get the situation of the result line
                    if situation not in ['Extinto', 'Registro de marca extinto']: #if not invalid
                        item_dict = {
                            'titulo': cols[3].text.strip(), #title / brand name
                            'situation': situation, #situation
                            'titular': cols[6].text.strip(), #owner
                            'data': cols[1].text.strip(), #date of expedition / priority (older is more important)
                        }
                        formatted_results.append(item_dict) #append to the formatted lis
            except Exception as exc:
                print('Erro ao processar linha:', exc)
                continue

        return formatted_results if formatted_results else None #return the formatted list
    except Exception as exc:
        print('Erro ao localizar resultados:', exc)
        return None
