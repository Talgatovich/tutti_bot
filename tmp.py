import requests

url = "http://www.notomania.ru/poisk.php"
data = {"question": "лето"}
response = requests.post(url=url, data=())
print(response.text)
