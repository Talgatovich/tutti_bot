import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent().random
headers = {"User-Agent": ua}

url = "https://musicnotes.info/"
data = {}
compositions_data = {}
page = requests.get(url=url, headers=headers)
soup = BeautifulSoup(page.text, "lxml")
my_list = soup.find_all(
    "span", class_="views-summary views-summary-unformatted"
)

for val in my_list:
    key = val.text[-2]
    value = val.a["href"]
    data[key] = value

# print(data)
# response = requests.get(url + value)


def search_author(second_name):
    current_url = url + data[second_name[0]]
    page = requests.get(current_url, headers=headers)
    soup = BeautifulSoup(page.text, "lxml")
    l = ""
    for link in soup.find_all("a"):
        if second_name in link.text:
            l = link.get("href")[1::]
            break
    compositions_url = url + l
    return compositions_url


def search_composition(compositions_url, title):
    response = requests.get(compositions_url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    pages = soup.find_all("li", class_="pager__item pager__item--last")
    for val in pages:
        max_page_num = int(val.a.get("href")[-1])
    url_list = []
    for i in range(max_page_num + 1):
        url = compositions_url + f"?instrument=All&amp%253=&page={i}"
        url_list.append(url)
    for url in url_list:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        compositions = soup.find_all(
            "td", class_="views-field views-field-title"
        )
        for item in compositions:
            key = item.text.strip()
            val = item.a["href"]
            compositions_data[key] = val
    for key in compositions_data.keys():
        if title in key:
            link = compositions_data[key]
            break
    return link


def download_notes(link):
    pass


# Пройти по ссылке, найти ссылку скачивания и узнать как передать клиенту скачанный файл
# Посмотри send_file для бота


compositions_url = search_author("Бах")
search_composition(compositions_url, "Рождественская")
