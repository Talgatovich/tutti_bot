import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent().random
HEADERS = {"User-Agent": ua}
URL = "https://musicnotes.info/"
ERROR_TEXT = (
    "К сожалению, такая композиция не найдена. "
    "Напишите мне чтобы поискать что-то ещё"
)


def main_page():
    """
    Парсит главную страницу(блок с алфавитным указателем) и возвращает словарь,
    в котором ключи - буквы алфавита, значения - ссылки.

    """
    data = {}
    try:
        page = requests.get(url=URL, headers=HEADERS)
    except Exception:
        return None
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
    """
    Принимает на вход фамилию автора и словарь из функции main_page.
    По фамилии находит страницу композиций автора и возвращает ссылку на неё
    """
    if len(second_name) == 0 or len(data) == 0:
        return None
    try:
        current_url = URL + data[second_name[0].upper()]
    except Exception:
        return None
    page = requests.get(url=current_url, headers=HEADERS)
    soup = BeautifulSoup(page.text, "lxml")
    tail = ""
    for link in soup.find_all("a"):
        if second_name.lower().strip() in link.text.lower():
            tail = link.get("href")[1::]
            compositions_url = URL + tail
            return compositions_url
    return None


def search_composition(compositions_url, title):
    """
    Принимает на вход ссылку на страницу с композициями определённого автора и
    название произведения, и возвращает ссылку на неё.
    """
    if len(title) == 0:
        return None
    compositions_data = {}
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
    """
    На странице произведения ищет ссылку на скачивание и возвращает её
    """
    if link is not None:
        response = requests.get(link, headers=HEADERS)
        soup = BeautifulSoup(response.text, "lxml")
        links = soup.find_all(
            "span",
            class_="file file--mime-application-zip file--package-x-generic",
        )

        if links == []:
            links = soup.find_all(
                "span",
                class_="field-content",
            )
        if links == []:
            links = soup.find_all(
                "div",
                class_="node__content",
            )
        if link == []:
            links = soup.find_all(
                "div",
                class_="view-content",
            )

        for val in links:
            dowload_link = val.a.get("href")
            if URL in dowload_link:
                return dowload_link
            elif "www.litres.ru" in dowload_link:
                return link
            return URL + dowload_link[1::]
    return ERROR_TEXT
