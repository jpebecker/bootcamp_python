from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ExpC
from selenium.webdriver.support.ui import WebDriverWait
class InternetTester:
    def __init__(self,DwSpeed,UpSpeed):
        self.url = 'https://www.speedtest.net/'
        self.download_speed = DwSpeed
        self.upload_speed = UpSpeed
        self.browser = webdriver.Chrome()

    def Test_Speed(self):
        self.browser.get(self.url)
        WebDriverWait(self.browser, 30).until(
            ExpC.visibility_of_element_located((By.CSS_SELECTOR, 'a.js-start-test.test-mode-multi'))
        )
        btn_start = self.browser.find_element(By.CSS_SELECTOR, 'a.js-start-test.test-mode-multi')
        btn_start.click()
        ###########################################################
        WebDriverWait(self.browser, 100).until(
            ExpC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[3]/div/div[3]/div/div[3]/div/div/div[1]/div/div/div[2]/div[2]/a'))
        )
        result_download = self.browser.find_element(
            By.CSS_SELECTOR, '.result-data-large.number.result-data-value.download-speed'
        ).text
        result_upload = self.browser.find_element(
            By.CSS_SELECTOR, '.result-data-large.number.result-data-value.upload-speed'
        ).text
        print(f'Velocidade de Download Calculada: {result_download}Mbps\n'
              f'Velocidade de Upload Calculada  : {result_upload}Mbps')

        if float(result_download) < self.download_speed or float(result_upload) < self.upload_speed:
            self.download_speed = float(result_download)
            self.upload_speed = float(result_upload)
            self.browser.quit()
            return False
        else:
            self.browser.quit()
            return True
