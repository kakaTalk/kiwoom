
import matplotlib.pyplot as plt
import mpl_finance
from  matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#db그리기 테스트임

from  DbControl import DbCon

class Draw:
    def __init__(self, pannel):
        self.fig = plt.figure(figsize=(12, 8))

        self.pannel = pannel
        self.canvas = FigureCanvas(self.fig)
        self.pannel.addWidget(self.canvas)

        self.make_subplot()

    def make_subplot(self):
        self.topAxax = self.fig.add_subplot(111)            #sub플롯의 크기를 조절 가능
        # self.bottomAxax = self.fig.subplot2grid((4, 4), (3, 0), rowspan=1, colspan=4)

    def draw_ohlc(self, data):  #data의 변동이 있을때만 다시 그리기
        self.topAxax.cla()
        mpl_finance.candlestick2_ohlc(self.topAxax, data['open'][-60:], data['high'][-60:], data['low'][-60:], data['close'][-60:], width=0.5, colorup='r', colordown='b')
        self.canvas.draw()




if __name__ == "__main__":          #db 그리기 완료
    d = Draw()
    # d.make_subplot()
    # db = DbCon("kospi.db")
    # data = db.read_db_to_dataframe(db.select_from_table("024060") + db.where('date', 20190101) + db.oreder_by('date'))
    # d.draw_ohlc(data)
    # plt.show()