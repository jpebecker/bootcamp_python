import requests
from bs4 import BeautifulSoup

request_page = requests.get('https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/')
request_page.raise_for_status()
request_page.encoding = 'utf-8'

page = BeautifulSoup(request_page.text,'html.parser')

titles = [item.get_text() for item in page.find_all(name='h3',class_='title')]
titles = titles[::-1]
#print(titles)

with open('titles.txt', 'w')as file:
    for title in titles:
        file.write(title)
        file.write('\n--------------------------------------------\n')