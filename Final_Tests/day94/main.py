import pyautogui,time
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

browser = webdriver.Chrome(options=options)
browser.get("https://elgoog.im/dinosaur-game/") #acess the site
time.sleep(3) #wait for loading the screen

checkbox = browser.find_element(By.ID, 'botStatus') #activate the site bot
checkbox.click()

time.sleep(1)  #wait to change url
pyautogui.press('space')  # start the game
