import os, time,requests,smtplib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from email.mime.text import MIMEText
###############################################Send email function
def send_email(message):
    email = MIMEText(message, _charset='utf-8')
    email['Subject'] = f'ALERTA: Preço de produto baixou'
    email['From'] = os.getenv('EMAIL_SENDER')
    email['To'] = 'jpebecker@gmail.com'
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:  # envia e-mail
        connection.starttls()
        connection.login(user=os.getenv('EMAIL_SENDER'), password=os.getenv('EMAIL_PASSWORD'))
        connection.sendmail(from_addr=os.getenv('EMAIL_SENDER'),
                            to_addrs='jpebecker@gmail.com',
                            msg=email.as_string())
        print('e-mail enviado')
############################################################Sheety
sheety_url = f"https://api.sheety.co/{os.getenv('sheety_id')}/amazonPricesApi/mainPage"
sheety_header = {
    "Authorization": f"Bearer {os.getenv('sheety_amazon_api_key')}"
}
sheety_request = requests.get(url=sheety_url, headers=sheety_header)
sheety_request.raise_for_status()

table = sheety_request.json()['mainPage']
#print(table)
table_prices = [float(item['price']) for item in table]
actual_prices_of_products = []

#################################################Config do Chrome para a amazon nao derrubar
options = Options()
options.add_argument("--headless")  # Roda sem abrir janela
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920x1080")
options.add_argument(os.getenv('browser_header'))

###############################################Inicializa o navegador
driver = webdriver.Chrome(options=options)

#webScraping
for item in table:
    print(f"Pesquisando item: {item['description']}")
    driver.get(item['hyperlink'])
    time.sleep(3)  #Tempo para pagina carregar

    page = BeautifulSoup(driver.page_source, 'html.parser')

    price_tag = page.find('span', class_='a-offscreen')
    if price_tag:
        price_text = price_tag.get_text().strip().replace('R$', '').replace('.', '').replace(',', '.')#parsing da string do texto
        price = float(price_text)
        actual_prices_of_products.append(price)
        print(f"Preço encontrado: R${price}")
    else:
        print("Preço não encontrado!")
        actual_prices_of_products.append(float('inf'))

    print("Trocando Item...\n")
    time.sleep(1)

driver.quit() #fecha o web-navegador
there_is_change = False
msg = ''
######################Compara os preços, envia email único e atualiza a tabela
for i in range(len(table_prices)):
    if actual_prices_of_products[i] < table_prices[i]:
        there_is_change = True
        print(f"Preço de {table[i]['description']} está menor! Enviando notificação por e-mail")
        ##################Sheety update
        body = {
            "mainpage" : {
                "price": actual_prices_of_products[i],
            }
        }
        sheety_header['Content-Type'] = 'application/json'
        new_sheety_request = requests.put(url=f"{sheety_url}/{i+2}", headers=sheety_header,json=body)
        new_sheety_request.raise_for_status()
        #################message concatenation
        msg += (f"\n{table[i]['description']} baixou de Preço!\n"
                f"De R${table_prices[i]} por R${actual_prices_of_products[i]}\n"
                f"Acesse o link: {table[i]['hyperlink']}\n\n")
if there_is_change:
    send_email(message=msg)
else:
    print('Sem mudanças de preço hoje')