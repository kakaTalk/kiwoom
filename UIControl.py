from  PyQt5.QtWidgets import  *
from  PyQt5.QtCore import  *
from  PyQt5 import uic
from  PyQt5.QtGui import  *
from  Kiwoom import KiwoomS
from Draw import Draw
from DbControl import DbCon
from datetime import datetime
import time


form_class = uic.loadUiType("trader.ui")[0]


#최종본은 이름을 코드로 변경#

class MyWindow(QMainWindow, form_class):
    def __init__(self, kiwoom):
        super().__init__()
        self.setupUi(self)          #formClass ui를 따오기 위해 사용


        self.drawGraph = Draw(self.verticalLayout)
        self.controlApi = kiwoom

        self.show_account()
        self.dbControl = DbCon("kospi.db")

        self.timerList = []     #타이머를 관리하는 리스트

        self.set_activity()
        self.set_connect_timer()

        self.userSeeChart = 0                   #사용자가 차트를 보는 중인지
        self.today = datetime.today().strftime("%Y%m%d")

    def show_account(self):
        n = int(self.controlApi._get_login_info("ACCOUNT_CNT"))
        acc_list = self.controlApi._get_login_info("ACCLIST" ).split(';')[0:n]
        self.comboBox.addItems(acc_list)


    def set_activity(self):
        self.lineEdit.returnPressed.connect(self.code_changed)
        self.lineEdit.textChanged.connect(self.stop_show_graph)
        self.pushButton.clicked.connect(self.store_day_ohlc)
        self.orderCash_btn.clicked.connect(self.send_order)

    def create_timer(self, sec):
        timer = QTimer(self)  #타이머 생성
        timer.start(sec)      #타이머 주기 설정
        return timer

    def store_day_ohlc(self):
        pass


    def set_connect_timer(self):                                #검증완료
        self.create_timer(1000).timeout.connect(self.timeout)
        self.create_timer(500).timeout.connect(self.renew_chart)
        self.create_timer(60000).timeout.connect(self.stop_show_graph)  #3분

    def stop_show_graph(self):
        self.userSeeChart = 0

    def view_ten_hoga(self):
        self.controlApi._set__opt10004(self.code)

        model = QStandardItemModel()
        for i in self.controlApi.hoga_list:
            model.appendRow(QStandardItem(i))

        self.hoga_list_view.setModel(model)

    def code_changed(self):
        name = self.lineEdit.text()
        self.code = self.controlApi.codeToName[name]

        self.lineEdit_2.setText(self.code)
        self.view_ten_hoga()
        self.userSeeChart = 1


    #ohlc비교해서 호가 날리기 호가는 조작가능 현재가만 알고 있으면 그 밑에 가격 알면 
    def renew_chart(self):
        if self.userSeeChart == 1:
            self.controlApi._set_opt10081(stock_code=self.code, date=self.today, prevNext=self.controlApi.nextValueHave)
            self.drawGraph.draw_ohlc(self.controlApi.ohlc)


    def send_order(self):
        order_type_lookup = {"신규매수": 1, "신규매도": 2, "매수취소":3, "매도취소":4}
        hoga_lookup = {"지정가": "00", "시장가": "03"}

        account = self.comboBox.currentText()
        order_type = self.comboBox_2.currentText()
        code = self.lineEdit_2.text()
        hoga = self.comboBox_3.currentText()
        num = self.spinBox_2.value()
        price = self.spinBox.value()

        self.controlApi._send_order("send_order_req", "0101", account, order_type_lookup[order_type], code, num, price, hoga_lookup[hoga], "")     #신규주문



    def timeout(self):
        current_time = QTime.currentTime()
        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time


        self.statusbar.showMessage(time_msg)