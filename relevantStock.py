import requests
from bs4 import BeautifulSoup

#시간이 오래 걸림 DB질의로 바꾸기
class pasingNaver:
    def __init__(self):
        self.name_change_upjong = {} #종목 이름 -> 종목 업종
        self.name_change_thema = {} #종목 이름 -> 종목 테마

        self.upjong_change_name = {}  # 종목 테마 -> 종목 이름
        self.thema_change_name = {}  # 종목 이름 -> 종목 테마

        self.get_theme_list()
        self.get_upjong_list()


    def get_upjong_list(self):
        url = "https://finance.naver.com/sise/sise_group.nhn?type=upjong"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")

        for i in soup.find_all('a'):        #a속성 모두 찾기
            cand = str(i)

            if "/sise/sise_group_detail" in cand:
                start = 0
                end = 0

                for index in range(1, len(cand)): #형식이 <>target<이런 식임
                    if cand[index] == '>':
                        start = index + 1

                    if cand[index] == '<':
                        end = index
                        break

                name_list = self.get_include_names("https://finance.naver.com" + i['href'])
                self.upjong_change_name[cand[start:end]] = name_list

                for name in name_list:
                    if name in self.name_change_upjong.keys():
                         self.name_change_upjong[name] = self.name_change_upjong[name] + cand[start:end] + "\n"
                    else:
                        self.name_change_upjong[name] = cand[start:end] + "\n"

    def get_theme_list(self):
        url = "https://finance.naver.com/sise/theme.nhn"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")

        for i in soup.find_all('a'):        #a속성 모두 찾기
            cand = str(i)

            if "/sise/sise_group_detail" in cand:
                start = 0
                end = 0

                for index in range(1, len(cand)): #형식이 <>target<이런 식임
                    if cand[index] == '>':
                        start = index + 1

                    if cand[index] == '<':
                        end = index
                        break

                name_list = self.get_include_names("https://finance.naver.com" + i['href'])
                self.thema_change_name[cand[start:end]] = name_list

                for name in name_list:
                    if name in self.name_change_thema.keys():
                         self.name_change_thema[name] = self.name_change_thema[name] + cand[start:end] + "\n"
                    else:
                        self.name_change_thema[name] = cand[start:end] + "\n"

    def get_include_names(self, upjong_address):
        soup = BeautifulSoup(requests.get(upjong_address).text, "lxml")
        name = []

        for i in soup.find_all('a'):
            cand = str(i)

            if "code" in cand:
                start = 0
                end = 0

                for index in range(1, len(cand)):
                    if cand[index] == '>':
                        start = index + 1

                    if cand[index] == '<':
                        end = index
                        break

                if len(cand[start:end]) >= 2:
                    name.append(cand[start:end])

        return name