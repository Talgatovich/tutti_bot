import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent().random
headers = {"User-Agent": ua}

url = "https://musicnotes.info/"
data = {}
authors_data = {}
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
    # print(soup)
    l = ""
    for link in soup.find_all("a"):
        if second_name in link.text:
            l = link.get("href")[1::]
            break
    print(l)
    compositions_url = url + l
    return compositions_url


def search_composition(compositions_url, title):
    pass


print(search_author("Eminem"))
