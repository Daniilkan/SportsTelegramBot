import random

from bs4 import BeautifulSoup
import requests

proxies = {
    'https': 'http://proxy.server:3128'
}

def get_adivice():
    filteredTips = []
    url = 'https://moneypapa.ru/kak-motivirovat-sebya-zanimatsa-sportom/'
    page = requests.get(url=url, proxies=proxies)
    html = page.text
    soup = BeautifulSoup(html, 'html.parser')
    allTips = soup.find_all('p')
    for i in allTips:
        if len(i.text) > 100:
            filteredTips.append(i.text)
    return random.choice(filteredTips)