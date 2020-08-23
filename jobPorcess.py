from queue import PriorityQueue
from datetime import datetime
import time
from PyQt5.QtCore import *


class priortyProcess(QThread):
    def __init__(self, callKiwoom):
        super().__init__()
        self.job_qp = PriorityQueue()

        self.callApi = callKiwoom
        self.api_call_count = 1

        self.canApiCall = 1
        self.today = datetime.today().strftime("%Y%m%d")
        self.setTime = int(time.strftime(time.strftime('%H%M%S')))  #몇초간격임을 알기 위한 것임

    def push(self, prior, name, code):
        self.job_qp.put([prior, name, code])

    def get_now_time(self):
        return int(time.strftime(time.strftime('%H%M%S')))  # 몇초간격임을 알기 위한 것임

    def set_now_time(self):
        self.setTime = int(time.strftime(time.strftime('%H%M%S')))  #몇초간격임을 알기 위한 것임

    #모든 실행은 여기서 관리함
    def excute(self):
        if self.job_qp.empty() == False:
            if self.api_call_count % 5 != 0 and self.canApiCall == 1:
                node = self.job_qp.get()  # 우선순위 제일 높은거

                if node[1] == "chart":  # 차트 갱신
                    self.callApi._set_opt10081(stock_code=node[2], date=self.today, prevNext=0)
                    self.callApi.stockName = self.callApi.codeToName[node[2]]

                elif node[1] == "hoga":     ##:
                    self.controlApi._set__opt10004(node[2])
                elif node[1] == "jango":
                    self.controlApi._set_opw00018(node[2], 2)

                self.set_now_time()
                self.api_call_count += 1

                return node[1]
            else:
                self.canApiCall = 0

                if self.get_now_time() - self.setTime >= 1:
                    self.api_call_count = 1
                    self.canApiCall = 1
        else:
            if self.get_now_time() - self.setTime >= 1:
                self.api_call_count = 1

        return "none"

    def run(self):
        pass



if __name__ == "__main__":
    pr = priortyProcess(1)

