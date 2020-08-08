from  PyQt5.QtWidgets import  *
from  PyQt5.QtCore import  *
from  PyQt5 import uic
from  Kiwoom import KiwoomS

form_class = uic.loadUiType("trader.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)          #formClass ui를 따오기 위해 사용
        self.set_activity()

        self.timer = QTimer(self)  #타이머 생성
        self.timer.start(1000)      #타이머 주기 설정
        self.timer.timeout.connect(self.timeout)


    def set_activity(self):
        self.lineEdit.returnPressed.connect(self.code_changed)

    def code_changed(self):
        code = self.lineEdit.text()
        print(code)
        name = KiwoomS.get_master_code_name(code)
        self.lineEdit_2.setText(code)

    def timeout(self):
        current_time = QTime.currentTime()
        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time


        self.statusbar.showMessage(time_msg)