from Kiwoom import *
import sys
from PyQt5.QtWidgets import *
from DbControl import *
from UIControl import MyWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

