from Kiwoom import *
import sys
from PyQt5.QtWidgets import *
from datetime import datetime
import time
from DbControl import *

app = QApplication(sys.argv)
k = KiwoomS()
db = DbCon("kospi.db")
k._login()

k._set_opt10081("024060", "20200805", 0)
print(k.ohlc)
print(k.nextValueHave)
time.sleep(0.5)
print(type(k.nextValueHave))

while k.nextValueHave == '2':
    print("진입")
    db.save_dataframe_to_db(k.ohlc, tableName="024060")
    k._set_opt10081("024060", "20200805", 2)
    print(k.ohlc)

    time.sleep(0.5)
