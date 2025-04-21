from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException
)
import time

########################3options para manter aberto o browser
chrome_options = wb.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = wb.Chrome(options=chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

timeout = time.time() + 5
five_min_timeout = time.time() + 60 * 5
#########################Loop principal
while True:
    try:
        #Busca o cookie
        cookie = driver.find_element(by=By.ID, value="cookie")
        cookie.click()
    except (StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException):
        print("Erro ao encontrar o cookie. Recarregando...")
        continue

    ###########################A cada 5 segundos#######################################33
    if time.time() > timeout:
        try:
            ################################################Busca os upgrades e preços de forma segura
            store_items = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")
            cookie_upgrades = {}

            for item in store_items:
                text = item.text
                if "-" in text:
                    try:
                        cost = int(text.split("-")[1].strip().replace(",", ""))
                        parent = item.find_element(By.XPATH, "..")  # volta para o div com id
                        upgrade_id = parent.get_attribute("id")
                        if upgrade_id:
                            cookie_upgrades[cost] = upgrade_id
                    except:
                        continue

            #######################################Atualiza quantos cookies tem
            money_element = driver.find_element(by=By.ID, value="money").text
            money_element = money_element.replace(",", "")
            cookie_count = int(money_element)

            ###############################Verifica quais upgrades são compraveis
            affordable_upgrades = {
                cost: id for cost, id in cookie_upgrades.items() if cookie_count > cost
            }

            if affordable_upgrades:
                ############################Compra o mais caro
                upgrade_mais_caro = max(affordable_upgrades)
                to_purchase_id = affordable_upgrades[upgrade_mais_caro]
                driver.find_element(by=By.ID, value=to_purchase_id).click()
                print(f"Upgrade comprado: {to_purchase_id} (gasto {upgrade_mais_caro} cookies)")

        except Exception as e:
            print(f"Erro durante consulta de upgrades: {e}")

        ###############################Atualiza o  timeout de 5 segundos
        timeout = time.time() + 5

    ####################a cada 5 minutos, mostra cookies por segundo
    if time.time() > five_min_timeout:
        try:
            cookie_per_s = driver.find_element(by=By.ID, value="cps").text
            print(f"\nAtualização: {cookie_per_s} cookies por segundo\n")
        except:
            print("\nErro ao identificar cookies por segundo\n")

