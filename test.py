import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":

    url = "https://finance.naver.com/sise/sise_group.nhn?type=upjong"
    target = "/sise/sise_group.nhn?type=upjong"
    res = requests.get(url)

    soup = BeautifulSoup(res.text, "lxml")
    print(soup)

    for i in soup.find_all('a'):
        if len(str(i)) >= len(url):
            sub = str(i)
            if "/sise/sise_group" in sub:
                print(str(i))
            else:
                pass
