from bs4 import BeautifulSoup
import requests,os,time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ExpC

website_clone_url = 'https://appbrewery.github.io/Zillow-Clone/'
forms_url = os.getenv('FORMS_URL')

page = requests.get(website_clone_url)
soup = BeautifulSoup(page.content, "html.parser")

unordered_card_list = soup.select_one(".List-c11n-8-84-3-photo-cards")
Lis = unordered_card_list.select('li')

properties = []

for li in Lis:
    addr_elem = li.select_one('[data-test="property-card-addr"]')
    address = addr_elem.get_text(strip=True).replace('|',',').replace('#','') if addr_elem else None
    price_elem = li.select_one('.PropertyCardWrapper__StyledPriceLine')
    if price_elem:
        txt = price_elem.text
        txt = (txt.replace('$','')
                  .replace('+','')
                  .replace('/mo','')
                  .replace('.',',')
                  .replace(',','')
                  .strip())
        price = float(txt.split()[0]) if txt else None
    else:
        price = None

    link_elem = li.select_one('[data-test="property-card-link"]')

    if link_elem:
        if link_elem.name == 'a' and link_elem.has_attr('href'):
            url = link_elem['href']
        else:
            a = link_elem.find('a')
            url = a['href'] if a and a.has_attr('href') else None
    else:
        url = None

    if address and price is not None and url:
        properties.append({
            'address': address,
            'price': price,
            'link': url
        })


print(f"Foram salvas {len(properties)} entradas válidas.")

print('\niniciando upload para planilha...')
for property in properties:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') #nao abre a janela
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=options)
    browser.get(forms_url)
    WebDriverWait(browser,15).until(ExpC.presence_of_element_located((By.CSS_SELECTOR,'input[type="text"]')))
    time.sleep(2)
    text_inputs = browser.find_elements(By.CSS_SELECTOR, 'input[type="text"]')

    values = [property['address'], property['price'], property['link']]
    for input, values in zip(text_inputs, values):
        input.send_keys(values)
        time.sleep(0.5)

    submit_btn = browser.find_element(By.CSS_SELECTOR, '[aria-label="Submit"]')
    submit_btn.click()
    time.sleep(1)
    browser.close()

print('Todas as entradas foram carregadas para o formulário')
