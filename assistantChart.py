import numpy as np
import math
class helpChart:
    def __init__(self):
        pass

    def change_log_data(self, data):
        result = []

        for i in range(len(data)):
            result.append(np.log(data[i]))

        return result

    def calc_avg(self, data, period):
        return data.rolling(period).mean()

    def calc_std(self, data, period):
        return data.rolling(period).std()

    def calc_var(self, data, period):
        return data.rolling(period).var()

    def calc_bolliger(self, org_data, period):
        k = 2

        avg_price = self.calc_avg(org_data, period)
        std_price = self.calc_std(org_data, period)

        upper_band = []
        mid_band = []
        lower_band = []

        for i in range(len(avg_price)):
            upper_band.append(avg_price[i] + (std_price[i] * k))
            lower_band.append(avg_price[i] - (std_price[i] * k))
            mid_band.append((upper_band[i] + lower_band[i]) / 2)

        return upper_band, mid_band, lower_band

    def normalization_data(self, data):
        avg_data = np.mean(data)
        std_data = np.std(data)

        result_data = []

        for i in range(len(data)):
            result_data.append((data[i] - avg_data) / std_data)

        return result_data
    
    #return이 없었음
    def normalization_data_spread(self, data1, data2, cov):
        resultData = []

        print("cov!!", cov)
        print("orgLog", data1)
        print("dataLog", data2)

        for i in range(len(data1)):
            resultData.append((data1[i] - cov * data2[i]) * 100)

        print("sperad_log", resultData)
        return resultData

    def get_prediction_profit(self, data):
        avg = np.mean(data)

        for i in range(len(data)):
            data[i] = data[i] - avg

        return data
    #                       data1에대한 data2의 cointegration 계수임
    def cointegration(self, org, calc_target):
        data1 = self.change_log_data(org)
        data2 = self.change_log_data(calc_target)

        if len(data2) != len(data1):
            return 0

        cov = np.cov(data1, data2)[0][1]

        print(np.cov(data1, data2), np.cov(data2, data1))
        var = np.var(data2)

        print("공분산 ", cov / var)
        return cov / var            #리스트 나누기 분산임

    def reSize_data(self, resultData, org_len):
        total_len = org_len - len(resultData)

        for idx in range(total_len):
            resultData.insert(0, resultData[0])

        return resultData

