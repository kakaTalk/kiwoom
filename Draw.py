
import matplotlib.pyplot as plt
import mpl_finance
import matplotlib.ticker
import datetime

#db그리기 테스트임

from  DbControl import DbCon

class Draw:
    def __init__(self):
        self.fig = plt.figure(figsize=(12, 8))
        self.make_subplot()

    def make_subplot(self):
        self.topAxax = plt.subplot2grid((4,4), (0,0), rowspan=3, colspan=4)            #sub플롯의 크기를 조절 가능
        self.bottomAxax = plt.subplot2grid((4, 4), (3, 0), rowspan=1, colspan=4)

    def draw_ohlc(self, data):
        mpl_finance.candlestick2_ohlc(self.topAxax, data['open'], data['high'], data['low'], data['close'], width=0.5, colorup='r', colordown='b')
        plt.draw()
        plt.show()



if __name__ == "__main__":          #db 그리기 완료
    d = Draw()
    # d.make_subplot()
    # db = DbCon("kospi.db")
    # data = db.read_db_to_dataframe(db.select_from_table("024060") + db.where('date', 20190101) + db.oreder_by('date'))
    # d.draw_ohlc(data)
    # plt.show()