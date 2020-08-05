from pandas import DataFrame
from datetime import datetime
from pykrx import stock

import math
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick2_ohlc

class strategy:

    def __init__(self, ohlc):
        self.ohlc = ohlc

    #data는 1차원
    def calc_exp(self, data, period):           #지수함수
        sum = 0
        resultData = []
        alpha = 2 / (period + 1)

        for idx in range(len(data)):
            if idx < period:
                sum += data[idx]

            if idx == (period - 1):
                resultData.append(((sum / period)))    #단순 평균구함

            if idx >= period:
                result = (alpha * data[idx] + ((1 - alpha) * resultData[len(resultData) - 1]))
                resultData.append(result)

        return resultData


    def calc_wilder(self, data, period):
        resultData = []
        sum = 0

        for idx in range(len(data)):
            sum += data[idx]

            if idx == (period - 1):
                resultData.append(sum / period)
            elif idx >= period:
                resultData.append(((resultData[len(resultData) - 1] * (period - 1)) + data[idx]) / period)

        return resultData

    def calc_avg(self, data, period):
        sum = 0
        resultData = []

        for idx in range(len(data)):
            sum += data[idx]

            if idx >= (period - 1):
                resultData.append(sum / period)
                sum -= data[idx - (period - 1)]

        return resultData

    def calc_dis(self, long, short):
        if len(long) != len(short):
            print("길이오류 ")
            return

        dis = []

        for i in range(len(long)):
            dis.append((short[i] / long[i]) * 100)

        return dis

    def find__buy_resultData_return(self, i):
        result_data = self.find_mv_avg_through(200, 20)
        return result_data

    def min(self, n1, n2):
        if n1 > n2:
            return n2
        return n1

    def max(self, n1, n2):
        if n1 > n2:
            return n1
        return n2


    def make_day_to_join(self, day):
        join_ohlc = {'open': [], 'high': [], 'low': [], 'close': [], 'volume': [], 'date': []}  # 초기화

        high = 0
        low = 987654321
        close = 0
        open = 0
        volume = 0

        #만약 day가 3일이라면
        for i in range(len(self.ohlc)):
            high = self.max(self.ohlc.loc[i]['high'], high)
            low = self.min(self.ohlc.loc[i]['low'], low)
            close = self.max(self.ohlc.loc[i]['close'], close)
            open = self.max(self.ohlc.loc[i]['open'], open)
            date = self.ohlc.loc[i]['date']

            volume += self.ohlc.loc[i]['volume']

            if (i % day) == 0:

                join_ohlc['open'].append(open)
                join_ohlc['high'].append(high)
                join_ohlc['low'].append(low)
                join_ohlc['close'].append(close)
                join_ohlc['date'].append(date)
                join_ohlc['volume'].append(volume)

                high = 0
                low = 987654321
                close = 0
                open = 0
                volume = 0

        join_ohlc = DataFrame(join_ohlc)
        return join_ohlc

    #원하는 데이터랑 날수 주면 돌파 하는지 알려줌
    def breakThrough(self, data, day, min_bt):
        result_data = []

        break_line = self.calc_avg(data['high'], day)
        break_line = self.reSize_data(break_line, len(data)) #데이터 길이 복원 작업

        volume_line = self.calc_avg(data['volume'], 2)
        volume_line = self.reSize_data(volume_line, len(data))

        print(len(data))
        for i in range(len(data)):
            date = data.loc[i]['date']
            low_price = data.loc[i]['low']
            close_price = data.loc[i]['close']
            high_price = data.loc[i]['high']

            if i > day and ((volume_line[i] * 1.3) <= data.loc[i]['volume']):                                              #거래량도 봐
                if low_price <= break_line[i] and break_line[i] <= high_price:
                    if (self.supportLine_disturb(break_line, i, 20, min_bt) == 1) and (close_price >= break_line[i]):  # supportList, nowIndex, supportDay):
                        result_data.append([close_price, date, i, 0])  # 2차원 배열 항상 명심

        return result_data

    def supportLine_disturb(self, supportList, nowIndex, supportDay, min_breakOut):


        if nowIndex - supportDay < 0:
            return 0                    #지지실패

        count = 0

        for i in range(1, supportDay):
            high = self.ohlc.loc[nowIndex - supportDay]['high']
            close = self.ohlc.loc[nowIndex - supportDay]['close']
            volume = self.ohlc.loc[nowIndex - supportDay]['volume']
            supPrice = supportList[nowIndex - supportDay]

            dis = (high / supPrice) * 100

            if (close < supPrice) and (97 <= dis and dis <= 100):
                count += 1

        if count >= min_breakOut:
            return 1

        return 0


    #일봉상 200일 돌파 전략 쓰렉임
    def find_mv_avg_through(self, long_mv, short_mv):       #시가총액 보고
        data = self.make_day_to_join(3)
        result_data = self.breakThrough(data, 20, 3)

        return result_data

    def reSize_data(self, resultData, org_len):
        resizeResult = []
        total_len = org_len - len(resultData)

        for idx in range(total_len):
            resultData.insert(0, resultData[0])

        return resultData

    def graph_show(self):
        fig = plt.figure(figsize=(12,8))

        top_axes = plt.subplot2grid((5,5), (0,0), rowspan=3, colspan=4)
        bottom_axes = plt.subplot2grid((5,5), (3,0), rowspan=1, colspan=4)
        bottom2_axes = plt.subplot2grid((5,5), (4,0), rowspan=1, colspan=4)

       # top_axes.plot(upAtr, color='r', linewidth = 2)

        r1 = self.find_get_signal()

        print(r1)
        r1 = self.reSize_data(r1, len(self.ohlc))

        top_axes.plot(r1,  color='r', linewidth = 2)

        candlestick2_ohlc(top_axes, self.ohlc['open'], self.ohlc['high'], self.ohlc['low'], self.ohlc['close'], width= 0.5)

        plt.show()



    #응용하면 지지 저항 구할 수 있을듯듯
    def calc_sar(slf, dataHigh, dataLow):
        resultdata = []
        uptrend = 1                     #1이면 상승추세 0이면 하락추세
        firstFindDay = 5                #0~4일까지임
        low = 987654321

        for idx in range(5):
            if low > dataLow[idx]:
                low = dataLow[idx]
        startaf = 0
        af = startaf
        jumpAf = 0.02
        maxAF = 0.2

        sar = low                   #초기 sar이라고 가정함
        resultdata.append(sar)
        ep = dataHigh[firstFindDay - 1] #초기 ep는 당일의 최고 값

        for idx in range(firstFindDay, len(dataHigh)):
            if uptrend == 1:                        #상승추세라면
                sar = int(sar + af * (ep - sar))
                resultdata.append(sar)


                if ep < dataHigh[idx]:              #상승값 갱신
                    ep = dataHigh[idx]
                    af = af + jumpAf
                    af = min(maxAF, af)

                if dataLow[idx] <= sar:         #추세 갱신에 실패함
                    uptrend = 0                 #하락 추세로 변경험
                    af = startaf

                    sar = ep                    #sar을 기준점을 변경함으로써 위에서 부터 내려올 수 있도록함
                    ep = dataLow[idx]
                    resultdata[len(resultdata) - 1] = sar


            else:          #하락추세fkqtRbfg9438
                sar = int(sar - af * (sar - ep))
                resultdata.append(sar)

                if ep > dataLow[idx]:
                    ep = dataLow[idx]
                    af = af + jumpAf
                    af = min(maxAF, af)

                if dataHigh[idx] >= sar:         #추세 갱신에 실패함
                    uptrend = 1                 #하락 추세로 변경험
                    af = startaf

                    sar = ep
                    ep = dataHigh[idx]
                    resultdata[len(resultdata) - 1] = sar

        print("sar",resultdata)
        return resultdata
