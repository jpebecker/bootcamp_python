import os,time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ExpC
from selenium.webdriver.support.ui import WebDriverWait
class X:
    def __init__(self):
        self.user = os.getenv('')
        self.key = os.getenv('')
        self.url = 'https://x.com/i/flow/login'
        self.browser = webdriver.Chrome()

def Post(actual:tuple,expected:tuple,browser,url):
    browser.get(url)
    msg = (f'Reclamação: Minha velocidade de internet está {actual[0]}Mbps Down e {actual[1]}Mbps Up\n'
            f'Contratei a operadora por {expected[0]}Mbps de Download e {expected[1]}Mbps de Upload\n'
            f'\nO que aconteceu? Podem me atualizar? @operadora\n')
    WebDriverWait(browser, 20).until(
        ExpC.presence_of_element_located((By.NAME, 'text'))
    )
    entry = browser.find_element(By.NAME,'text')
    entry.click()
    entry.send_keys(os.getenv('X_USERNAME'))
    entry.send_keys(Keys.ENTER)
    WebDriverWait(browser,10).until(ExpC.presence_of_element_located((By.NAME,"password")))
    p_entry = browser.find_element(By.NAME,'password')
    p_entry.click()
    p_entry.send_keys(os.getenv('X_PASSWORD'))
    p_entry.send_keys(Keys.ENTER)
    WebDriverWait(browser,60).until(ExpC.url_to_be('https://x.com/home'))

    post_entry = WebDriverWait(browser, 10).until(ExpC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="textbox"]')))
    post_entry.send_keys(msg)

    publish_button = WebDriverWait(browser, 10).until(ExpC.presence_of_element_located((By.CSS_SELECTOR,'[data-testid="tweetButtonInline"]')))
    publish_button.click()
    time.sleep(5) #tempo para publicar...

    print('Reclamação Publicada!')
    browser.quit()