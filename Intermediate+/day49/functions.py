from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpCondt
from selenium.common.exceptions import StaleElementReferenceException
import os,time,json

def login(browser, wait, keywords,location):
    user_entry = wait.until(ExpCondt.element_to_be_clickable((By.ID, 'username')))
    user_entry.send_keys(os.getenv('linkedin_user'))

    password_entry = wait.until(ExpCondt.element_to_be_clickable((By.ID, 'password')))
    password_entry.send_keys(os.getenv('linkedin_password'))

    enter_button = wait.until(ExpCondt.element_to_be_clickable((By.XPATH, '//*[@id="organic-div"]/form/div[4]/button')))
    enter_button.click()

    #Espera a barra de busca carregar
    wait.until(ExpCondt.presence_of_element_located((By.XPATH, '//*[@id="global-nav-typeahead"]/input')))

    search(browser, wait,keywords,location)

def search(browser, wait,keywords,location):
    search_box = wait.until(ExpCondt.element_to_be_clickable((By.XPATH, '//*[@id="global-nav-typeahead"]/input')))
    search_box.click()

    for word in keywords:
        search_box = wait.until(ExpCondt.element_to_be_clickable((By.XPATH, '//*[@id="global-nav-typeahead"]/input')))
        search_box.clear()
        search_box.send_keys(word.strip())
        search_box.send_keys(Keys.ENTER)

        #Espera os filtros aparecerem e clica em VAGAS
        wait.until(ExpCondt.element_to_be_clickable(
            (By.XPATH, '//*[@id="search-reusables__filters-bar"]/ul/li[1]/button'))).click()

        #Chama Get_appliance() para processar e salvar as vagas
        get_appliance(browser, keywords, location)

def get_appliance(browser, keywords, location):
    wait = WebDriverWait(browser, 10)
    saved_jobs = []
    #####################################################################INSERE A LOCATION COMO FILTRO
    location_entry = wait.until(ExpCondt.presence_of_element_located(
        (By.XPATH, '//input[contains(@id, "jobs-search-box-location")]')))

    location_entry.click()
    location_entry.clear()
    location_entry.send_keys(location)

    location_btn = wait.until(ExpCondt.element_to_be_clickable(
        (By.XPATH, '//*[@id="global-nav-search"]/div/div[2]/button[1]')))

    location_btn.click()
    time.sleep(2)
    ###########################################################################PEGA A UNORDERED LIST E SEUS LIST INSTANCES
    ul_xpath = '//*[@id="main"]/div/div[2]/div[1]/div/ul'
    ul = wait.until(ExpCondt.presence_of_element_located((By.XPATH, ul_xpath)))
    lis = ul.find_elements(By.TAG_NAME, 'li')
    ################################################MANIPULACAO DAS LIS (VAGAS)
    last_item_title = ''
    last_item_emp = ''
    for li in lis:
        try:
            browser.execute_script("arguments[0].scrollIntoView(true);", li) #DEIXA A VISTA DA TELA
            time.sleep(1)
            li.click() #CLICA NO LI
            time.sleep(1.5) #AGUARDA

            #Coleta o título do (cargo) NA ABA LATERAL (DIREITA da page)
            title_el = wait.until(ExpCondt.presence_of_element_located(
                (By.XPATH, '//main//h1')))
            title = title_el.text.strip()

            #Coleta o nome da empresa na ABA LATERAL (DIREITA)
            company_el = wait.until(ExpCondt.presence_of_element_located((
                By.XPATH,
                '//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div[1]/div[1]/div/a')))
            company = company_el.text.strip()

            if title != last_item_title and company != last_item_emp:#VERIFICA SE JA VIU ESTA VAGA NA ULTIMA VERF
                print(f">>> Cargo: {title} | Empresa: {company}")
                last_item_title = title
                last_item_emp = company
                ###############Separa o title do cargo em palavras
                title_words = set(title.lower().split(' '))
                #Verifica se alguma keyword corresponde a uma palavra no título
                for keyword in keywords:
                    if any(word.startswith(keyword.strip().lower()) for word in title_words): #SE O TITULO TIVER ALGUMA KEYWORD
                        print(f">>> Palavra-chave '{keyword}' encontrada em: {title}")
                        ###############Salva a vaga
                        save_button = wait.until(ExpCondt.element_to_be_clickable((
                            By.XPATH,
                            '//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div[5]/div/button/span[1]')))
                        save_button.click()
                        time.sleep(1)
                        saved_jobs.append({'cargo': title, 'empresa': company})
                        print('>>> VAGA SALVA')
                        break
                    else:
                        print('>>> Vaga não corresponde aos Keywords')
                        break
            else:
                print('.')
        except StaleElementReferenceException:
            print(f">>> Status da Vaga: stale, pulando...")
        except Exception as e:
            print(f">>> Erro na vaga:", e)

    #salva as vagas em um json
    if saved_jobs:
        with open('vagas_salvas.json', 'w', encoding='utf-8') as file:
            json.dump(saved_jobs, file, ensure_ascii=False, indent=4)

        browser.quit()  # fecha navegador após feito arquivo .json
        return print("\n>>> Vagas salvas com sucesso em 'vagas_salvas.json'")
    else:
        browser.quit()  # fecha navegador
        return print("\n>>> Nenhuma vaga correspondente encontrada'")