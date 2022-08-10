import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent().random
headers = {'User-Agent': ua}

url = "http://www.notomania.ru/"
data = {"question": "лето"}
page = requests.get(url=url, headers=headers) # data=('Бах').encode('utf-8'))
soup = BeautifulSoup(page.text, "html.parser")
soup.encode('utf-8').decode('utf-8')
print(soup)
