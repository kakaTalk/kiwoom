from Kiwoom import *
import sys
from PyQt5.QtWidgets import *
from DbControl import *
from UIControl import MyWindow
import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoomApi = KiwoomS()       #키움 api호출하는 클래스
    myWindow = MyWindow(kiwoomApi)      #UI를 조작하는 클래스
    myWindow.show()
    app.exec_()

