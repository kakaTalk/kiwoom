import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class analytics:
    def __init__(self, stockList):      #i랑 밀접하게 연관있는 종목 찾음
        self.stockList = stockList


    def findConv(self, stockName):
        resultData = []
        print(stockName)
        target = self.stockList[stockName]['close']
        #상관관계가 높은 5개만 찾고 싶음
        for i in self.stockList.keys():
            if i == stockName:
                continue
            else:
                if len(target) == len(self.stockList[i]['close']):
                    result = np.corrcoef(target, self.stockList[i]['close'])
                    resultData.append((result[0][1], i))

        resultData.sort(reverse=True)
        return resultData[0:5]

