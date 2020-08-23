import matplotlib.pyplot as plt
import mpl_finance
from  matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import *
from assistantChart import helpChart
from matplotlib import font_manager, rc

#db그리기 테스트임

from  DbControl import DbCon

class Draw(QThread):
    def __init__(self, pannel):
        super().__init__()

        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=font_name)

        self.fig = plt.figure()

        self.pannel = pannel
        self.canvas = FigureCanvas(self.fig)
        self.pannel.addWidget(self.canvas)

        self.make_subplot()

        self.calc_chart = helpChart()

        self.orgData = {}    #이 종목이 기점
        self.data = {}          #이 종목이 구하고 싶은거
        self.start = 0
        self.stockName = "메모"
        self.cov = -1.0

    def make_subplot(self):
        self.topAxax = plt.subplot2grid((6, 6), (0, 0), rowspan=3, colspan=6)
        self.midAxax = plt.subplot2grid((6, 6), (3, 0), rowspan=2, colspan=6)
        self.bottomAxax = plt.subplot2grid((6, 6), (5, 0), rowspan=1, colspan=6)

    def draw_ohlc(self):  #data의 변동이 있을때만 다시 그리기
        self.topAxax.cla()
        mpl_finance.candlestick2_ohlc(self.topAxax, self.data['open'][-self.start:], self.data['high'][-self.start:], self.data['low'][-self.start:], self.data['close'][-self.start:], width=0.5, colorup='r', colordown='b')

    def draw(self, target, start, label):
        self.topAxax.plot(target[-start:], label = label)

    def bottom_draw(self):
        self.bottomAxax.cla()

        t_avg = self.calc_chart.normalization_data(self.orgData['close'])
        cand_avg = self.calc_chart.normalization_data(self.data['close'])

        self.bottomAxax.plot(t_avg[-self.start:], label= "타켓")
        self.bottomAxax.plot(cand_avg[-self.start:], label = self.stockName)
        
    def mid_draw(self):
        self.midAxax.cla()

        logOrg = self.calc_chart.change_log_data(self.orgData['close'])
        logData = self.calc_chart.change_log_data(self.data['close'])
        spread = self.calc_chart.normalization_data_spread(logOrg, logData, self.cov)
        res = self.calc_chart.get_prediction_profit(spread)

        self.midAxax.scatter(x=range(len(res[-self.start:])), y=res[-self.start:], c='k')
        self.midAxax.plot(res[-self.start:], label = "밑에 같음")
        
    def set_legend(self):
        self.topAxax.legend()  # 라벨에 따른 자동 범례
        self.midAxax.legend()
        self.bottomAxax.legend()  # 라벨에 따른 자동 범례

    #그래프 처리 여기서 다 함
    def run(self):
        self.draw_ohlc()  # 여기서 오류남
        avg = self.calc_chart.calc_avg(self.data['high'], 200)
        band_data = self.calc_chart.calc_bolliger(self.data['high'], 60)

        self.draw(band_data[0], self.start, "upper")
        self.draw(band_data[1], self.start, "mid")
        self.draw(band_data[2], self.start, "down")
        self.draw(avg.tolist(), self.start, "200avg")

        print("상관계수 구하로 감")
        cand_cov = self.calc_chart.cointegration(self.orgData['close'], self.data['close'])     #오류내용 데이터 프레임을 통째로 넘겨줘서 그럼 뽑아서 시리즈로 넘겨야하는데

        if abs(1 - cand_cov) < abs(1 - self.cov):
            print(abs(1 - cand_cov), abs(1 - self.cov))
            self.cov = cand_cov
            self.bottom_draw()
            self.mid_draw()

        self.set_legend()
        self.canvas.draw()

if __name__ == "__main__":          #db 그리기 완료
    d = Draw()
    # d.make_subplot()
    # db = DbCon("kospi.db")
    # data = db.read_db_to_dataframe(db.select_from_table("024060") + db.where('date', 20190101) + db.oreder_by('date'))
    # d.draw_ohlc(data)
    # plt.show()