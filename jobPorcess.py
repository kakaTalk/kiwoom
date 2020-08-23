from queue import PriorityQueue
from datetime import datetime
import time


class priortyProcess:
    def __init__(self, callKiwoom):
        self.job_qp = PriorityQueue()

        self.callApi = callKiwoom
        self.undo_use = -1  #-1 사용 x 나머지는 최근 사용한 시간 api
        self.api_call_count = 0


        self.today = datetime.today().strftime("%Y%m%d")
        self.nowTime = time.strftime(time.strftime('%H%M%S'))

        print(self.nowTime)
        print(self.today)

    def push(self, prior, code):
        self.job_qp.put([prior, code])

    #모든 실행은 여기서 관리함
    def excute(self):

        if self.job_qp.empty() == False:
            first_ex = self.job_qp.get()  # 우선순위 제일 높은거 가져옴
            print(first_ex)

            if first_ex[0] == 3:  # 차트 갱신
                print("실행")
                self.callApi._set_opt10081(stock_code=first_ex[1], date=self.today, prevNext=self.callApi.nextValueHave)
                print(self.callApi.ohlc)


if __name__ == "__main__":
    pr = priortyProcess(1)

