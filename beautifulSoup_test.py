import requests
from bs4 import BeautifulSoup

# スクレイピング対象の URL にリクエストを送り HTML を取得する
# res = requests.get('http://127.0.0.1:5500/imgtest.html')

with open("./imgtest.html","r",encoding="utf-8") as read_html:
    read_data = read_html.read()
# レスポンスの HTML から BeautifulSoup オブジェクトを作る
soups = BeautifulSoup(read_data, 'html.parser')

# ページに含まれるリンクを全て取得する
links = [url.get('href') for url in soups.find_all('a')]
print(links[5])
link = str(links[5])

print(link.split("/"))

link_split = link.split("/")

print(link_split[-1])

link_name = link_split[-1]

print(link_name.split("."))

file_name = link_name.split(".")

print(file_name[-2])


res = requests.get('http://127.0.0.1:5500/imgtest.html')

soup = BeautifulSoup(res.text, 'html.parser')

link = [url.get('src') for url in soup.find_all('img')]
print(link)



