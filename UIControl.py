from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtGui import *
from Kiwoom import KiwoomS
from Draw import Draw
from DbControl import DbCon
from datetime import datetime
from relevantStock import pasingNaver
from jobPorcess import priortyProcess
from assistantChart import helpChart

form_class = uic.loadUiType("trader.ui")[0]


# 최종본은 이름을 코드로 변경#
#각각의 데이터의 길이가 다를 수 있음

class MyWindow(QMainWindow, form_class):
    def __init__(self, kiwoom):
        super().__init__()
        self.setupUi(self)  # formClass ui를 따오기 위해 사용

        # 클래스 생성하는 공간
        self.find_relevant_stock = pasingNaver()
        self.drawGraph = Draw(self.verticalLayout)
        self.jobStandby = priortyProcess(kiwoom)
        self.helpChartUnd = helpChart()
        self.controlApi = kiwoom

        self.show_account()  # 계좌 보이게하는 함수
        self.dbControl = DbCon("kospi.db")

        self.set_activity()

        self.userSeeChart = 0  # 사용자가 차트를 보는 중인지
        self.today = datetime.today().strftime("%Y%m%d")

        self.set_connect_timer()

        self.targetData = {}  # 이 종목과 다른 종목의 스프레드를 구하고 싶음

    def show_account(self):
        n = int(self.controlApi._get_login_info("ACCOUNT_CNT"))
        acc_list = self.controlApi._get_login_info("ACCLIST").split(';')[0:n]
        self.comboBox.addItems(acc_list)

        self.controlApi._set_opw00018(acc_list[0], 2)
        self.tableWidget.setRowCount(len(self.controlApi.accInfo))

        for i in range(len(self.controlApi.accInfo)):
            row = self.controlApi.accInfo.iloc[i]
            for j in range(len(row)):
                item = QTableWidgetItem(str(row[j]))
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.tableWidget.setItem(i, j, item)

    def set_activity(self):
        self.lineEdit.returnPressed.connect(self.search_chart)
        self.lineEdit.textChanged.connect(self.stop_show_graph)
        self.pushButton.clicked.connect(self.store_day_ohlc)
        self.orderCash_btn.clicked.connect(self.send_order)

    def create_timer(self, sec):
        timer = QTimer(self)  # 타이머 생성
        timer.start(sec)  # 타이머 주기 설정
        return timer

    def store_day_ohlc(self):
        pass

    def set_connect_timer(self):  # 검증완료
        self.create_timer(1000).timeout.connect(self.timeout)
        self.create_timer(500).timeout.connect(self.job_exec)


    #잡 실행해서 받아오는 함수
    def job_exec(self):
        job = self.jobStandby.excute()

        if job == "chart":
            print("차트진입됨")
            self.drawGraph.data = self.controlApi.ohlc
            self.drawGraph.start = self.spinBox_3.value()
            self.drawGraph.stockName = self.controlApi.stockName
            print("그리기 진입", self.drawGraph.stockName)

            if self.drawGraph.stockName == self.lineEdit.text():
                self.drawGraph.orgData = self.controlApi.ohlc
            else:
                self.drawGraph.run()
                print("종료")


    def stop_show_graph(self):
        self.userSeeChart = 0

    def view_ten_hoga(self):
        model = QStandardItemModel()

        for i in self.controlApi.hoga_list:
            model.appendRow(QStandardItem(i))

        self.hoga_list_view.setModel(model)

    # 리스트인데 문자열로 연결을 할려고 해서 그럼 오류내용 1
    #무슨 오류인지 적어 놓기
    def search_chart(self):
        name = self.lineEdit.text()
        self.code = ""

        if name in self.controlApi.nameToCode.keys():
            self.code = self.controlApi.nameToCode[name]
            upjong = ""
            thema = ""

            print("코드를 찾나 봄 ", self.code)

            #초기데이터 설정
            self.draw_chart(self.code)
            self.jobStandby.excute()
            self.drawGraph.orgData = self.controlApi.ohlc
            self.drawGraph.cov = -1

            if name in self.find_relevant_stock.name_change_upjong.keys():
                upjong = self.find_relevant_stock.name_change_upjong[name]
                upjongName = upjong.split()

                for i in upjongName:
                    nameList = self.find_relevant_stock.upjong_change_name[i]
                    print(nameList)

                    for get_names in nameList:
                        if get_names in self.controlApi.nameToCode.keys():
                            self.draw_chart(self.controlApi.nameToCode[get_names])

            if name in self.find_relevant_stock.name_change_thema.keys():
                thema = self.find_relevant_stock.name_change_thema[name]

            self.textEdit.setText(upjong + thema)
            self.lineEdit_2.setText(self.code)



    # ohlc비교해서 호가 날리기 호가는 조작가능 현재가만 알고 있으면 그 밑에 가격 알면
    def draw_chart(self, code):
        self.jobStandby.push(3, "chart", code)

    def renew_hoga(self):
        self.jobStandby.push(1, "hoga", self.code)

    def renew_jango(self):
        # 콤보박스에서 얻어서 날림
        self.jobStandby.push(2, "hoga", "COMV")

    def send_order(self):
        order_type_lookup = {"신규매수": 1, "신규매도": 2, "매수취소": 3, "매도취소": 4}
        hoga_lookup = {"지정가": "00", "시장가": "03"}

        account = self.comboBox.currentText()
        order_type = self.comboBox_2.currentText()
        code = self.lineEdit_2.text()
        hoga = self.comboBox_3.currentText()
        num = self.spinBox_2.value()
        price = self.spinBox.value()

        self.controlApi._send_order("send_order_req", "0101", account, order_type_lookup[order_type], code, num, price,
                                    hoga_lookup[hoga], "")  # 신규주문

    def timeout(self):
        current_time = QTime.currentTime()
        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time

        self.statusbar.showMessage(time_msg)
