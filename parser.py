import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent().random
HEADERS = {"User-Agent": ua}
URL = "https://musicnotes.info/"


compositions_data = {}


def main_page():
    data = {}
    page = requests.get(url=URL, headers=HEADERS)
    soup = BeautifulSoup(page.text, "lxml")
    my_list = soup.find_all(
        "span", class_="views-summary views-summary-unformatted"
    )

    for val in my_list:
        key = val.text[-2]
        value = val.a["href"]
        data[key] = value
    return data


def search_author(second_name, data):
    if len(second_name) == 0:
        return None
    current_url = URL + data[second_name[0].upper()]
    page = requests.get(url=current_url, headers=HEADERS)
    soup = BeautifulSoup(page.text, "lxml")
    tail = ""
    for link in soup.find_all("a"):
        if second_name.lower() in link.text.lower():
            tail = link.get("href")[1::]
            compositions_url = URL + tail
            return compositions_url
    return None


def search_composition(compositions_url, title):
    if len(title) == 0:
        return None
    if compositions_url is not None:
        response = requests.get(compositions_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "lxml")
        pages = soup.find_all("li", class_="pager__item pager__item--last")
        max_page_num = 0
        for val in pages:
            max_page_num = int(val.a.get("href")[-1])
        url_list = []
        for i in range(max_page_num + 1):
            url = compositions_url + f"?instrument=All&amp%253=&page={i}"
            url_list.append(url)
        for url in url_list:
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.text, "lxml")
            compositions = soup.find_all("a")
            for item in compositions:
                key = item.text.strip()
                val = item["href"]
                compositions_data[key] = val
        for key in compositions_data.keys():
            if title.lower() in key.lower():
                link = compositions_data[key][1::]
                return URL + link
    return None


def download_notes(link):
    if link is not None:
        response = requests.get(link, headers=HEADERS)
        soup = BeautifulSoup(response.text, "lxml")
        links = soup.find_all(
            "span",
            class_="file file--mime-application-zip file--package-x-generic",
        )  # 'clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item'
        if links == []:
            links = soup.find_all(
                "span",
                class_="field-content",
            )
        print(links)
        for val in links:
            dowload_link = val.a.get("href")
            return dowload_link
    return "К сожалению, такая композиция не найдена"


# Пройти по ссылке, найти ссылку скачивания и узнать как передать клиенту скачанный файл
# Посмотри send_file для бота
# Придумать решение если нет такого названия в базе

data = main_page()
compositions_url = search_author("Blackmore's Night", data)
link = search_composition(compositions_url, "Wish you")
print(download_notes(link))
