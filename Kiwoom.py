from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from pandas import DataFrame

#내일은 일봉 데이터 뽑아오는거 원하는 날짜에서 ~ 어디까지 더 간다면 테스트까지

class KiwoomS(QAxWidget):
    def __init__(self):
        super().__init__()

        self._create_kiwoom_instance()
        self.set_signol_slot()

        self.nextValueHave = 0      #다음 값이 있는지 체크해줌
        self.codeToName = {}

        #로그인
        self._login()
        #종목코드 갱신
        self.code_to_name()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    # LOGin
    def _login(self):
        self.dynamicCall("CommConnect()")
        self.onEvent = QEventLoop()
        self.onEvent.exec()

    def _get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(Qstring)", tag)
        return ret

    #코스닥 코스피 종목코드 갱신
    def code_to_name(self):
        code_list = self.get_code_list_by_market(0)

        for i in self.get_code_list_by_market(10):
            code_list.append(i)

        for i in code_list:
            self.codeToName[self.get_master_code_name(i)] = i

    # Event CallBack
    def set_signol_slot(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._OnReceiveTrData)
        self.OnReceiveChejanData.connect(self._OnReceiveChejanData)

    def _get_connect_state(self):
        ret = self.dynamicCall("GetConnectState()")
        return ret

    def _event_connect(self, err_code):
        if err_code == 0:
            print("로그인성공")
        else:
            print("로그인 실패" + err_code)

        self.onEvent.exit()

    def _CommRqData(self, rq_name, tr_name, prevNext):
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rq_name, tr_name, prevNext, "0101")
        self.onEvent = QEventLoop()
        self.onEvent.exec()

    def _OnReceiveChejanData(self, gubun, iten_cnt, fid_list):
        print(gubun)
        print("fidList" + fid_list)

        print(self.get_chejan_data(302))    #종목명
        print(self.get_chejan_data(900))    #"주문수량"
        print(self.get_chejan_data(901))    #"901" : "주문가격"
        self.onEvent.exit()


    def get_chejan_data(self, fid):
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    def _send_order(self, rqname, screen_no, account, order_type, code, num, price, hoga, orderNo):
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                         [rqname, screen_no, account, order_type, code, num, price, hoga, orderNo])

        self.onEvent = QEventLoop()
        self.onEvent.exec()


    #코드 가져오는 함수
    def get_code_list_by_market(self, market):
        codeList = self.dynamicCall("GetCodeListByMarket(QString)", market)
        codeList = codeList.split(';')
        return codeList[:-1]

    def get_master_code_name(self, market):
        codeName = self.dynamicCall("GetMasterCodeName(QString)", market)
        return codeName

    #조회하기 전에 값을 넣는 함수
    def _SetInputValue(self, id, code):
        self.dynamicCall("SetInputValue(QString, QString)", id, code)


                                                                               #사용안함
    def _OnReceiveTrData(self, scrNo, rq_name, tr_name, recode_name, prevNext,  dl, err_code, msg, msg1):
        self.nextValueHave = prevNext

        if rq_name == "opt10001_req":
            self._get__opt10001(tr_name, recode_name, prevNext)
        #일봉 조회
        elif rq_name == "opt10081_req":
            self._get_opt10081(tr_name, recode_name, prevNext)
        elif rq_name == "opt10060_req":
            self._get_opt10060(tr_name, recode_name, prevNext)
        elif rq_name == "opt20006_req":
            self._get_opt20006(tr_name, recode_name, prevNext)
        elif rq_name == "opt20002_req":
            self._get_opt20002(tr_name, recode_name, prevNext)
        elif rq_name == "opt10030_req":
            self._get_opt10030(tr_name, recode_name, prevNext)
        elif rq_name == "opt10080_req":
            self._get_opt10080(tr_name, recode_name, prevNext)
        elif rq_name == "opt10082_req":
            self._get_opt10082(tr_name, recode_name, prevNext)

        self.onEvent.exit()


    #_opt10001          함수 호출완료 event받아야 함
    def _set__opt10001(self, value):
        self._SetInputValue("종목코드", value)
        self._CommRqData("opt10001_req", "opt10001", 0)

    #데이터 받아오는 함수
    def _get__opt10001(self, tr_name, recode_name, index):
        self.stockName = self._GetCommData(tr_name, recode_name, index, "종목명")     #어쩔 수 없이 얻을꺼 "현재가처럼 output보고 지정"
        self.market_amount = self.erase_strip(self._GetCommData(tr_name, recode_name, index, "시가총액")) #시가 총액 받음
        self.stockNumber = self.erase_strip(self._GetCommData(tr_name, recode_name, index, "상장주식"))  # 시가 총액 받음

    #GetCommData                                     tr 에서 얻어오려는 항목 이름
    def _GetCommData(self, tr_name, recode_name, index, tr_get_name):
        data = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_name, recode_name, index, tr_get_name)
        return data.strip()


    def _set_opt10047(self, tr_name, recode_name, index):
        n = self.dynamicCall("GetRepeatCnt(QString, QString)", tr_name, recode_name)

    #당일
    def _set_opt10030(self, market, std, volume, pricestd, priceVolume, working):
        self.rankVolume = {'code': [], 'turnOver': [], 'price': []}  # 초기화

        self._SetInputValue("시장구분", market)
        self._SetInputValue("정렬구분", std)
        self._SetInputValue("괸리종목포함", "14")
        self._SetInputValue("신용구분", "0")
        self._SetInputValue("거래량구분", volume)
        self._SetInputValue("가격구분", pricestd)
        self._SetInputValue("거래대금구분", priceVolume)
        self._SetInputValue("장운영구분", working)

        self._CommRqData("opt10030_req", "opt10030", 0)

    def _get_opt10030(self, tr_name, recode_name, index):
        n = self.dynamicCall("GetRepeatCnt(QString, QString)", tr_name, recode_name)

        for i in range(n):
            code = self._GetCommData(tr_name, recode_name, i, "종목코드")
            change = self._GetCommData(tr_name, recode_name, i, "거래회전율")
            price = self._GetCommData(tr_name, recode_name, i, "현재가")

            self.rankVolume['code'].append(code)
            self.rankVolume['turnOver'].append(self.stringToNum(change))
            self.rankVolume['price'].append(abs(self.stringToNum(price)))

        self.rankVolume = DataFrame(self.rankVolume)

    #시장구분 = 0:코스피, 1: 코스닥, 2: 코스피200
    def _set__opt20002(self, market, value):
        self._SetInputValue("시장구분", market)
        self._SetInputValue("업종코드", value)
        self._CommRqData("opt20002_req", "opt20002", 0)

    def _get_opt20002(self, tr_name, recode_name, index):
        self.market_and_code = []

        n = self.dynamicCall("GetRepeatCnt(QString, QString)", tr_name, recode_name)

        for n in range(n):
            code = self._GetCommData(tr_name, recode_name, n, "종목코드")
            self.market_and_code.insert(0, code)

        self.market_and_code = DataFrame(self.market_and_code)

    def _set_opt20006(self, id, date):
        self.ohlc = {'open': [], 'high': [], 'low': [], 'close': [], 'volume': [], 'date': []}  # 초기화
        self._SetInputValue("업종코드", id)
        self._SetInputValue("기준일자", date)
        self._CommRqData("opt20006_req", "opt20006", 0)


    def _get_opt20006(self, tr_name, recode_name, index):
        n = self.dynamicCall("GetRepeatCnt(QString, QString)", tr_name, recode_name)

        for n in range(n):
            open = self._GetCommData(tr_name, recode_name, n, "시가")
            close = self._GetCommData(tr_name, recode_name, n, "현재가")
            high = self._GetCommData(tr_name, recode_name, n, "고가")
            low = self._GetCommData(tr_name, recode_name, n, "저가")
            date = self._GetCommData(tr_name, recode_name, n, "일자")
            volume = self._GetCommData(tr_name, recode_name, n, "거래량")

            self.ohlc['open'].insert(0, self.erase_strip(open))
            self.ohlc['close'].insert(0, self.erase_strip(close))
            self.ohlc['high'].insert(0, self.erase_strip(high))
            self.ohlc['low'].insert(0, self.erase_strip(low))
            self.ohlc['date'].insert(0, self.erase_strip(date))
            self.ohlc['volume'].insert(0, self.erase_strip(volume))

        self.ohlc = DataFrame(self.ohlc)


    def _set_opt10060(self, date, code, money, type, unit):
        self._SetInputValue("일자", date)
        self._SetInputValue("종목코드", code)
        self._SetInputValue("금액수량구분", money)
        self._SetInputValue("매매구분", type)
        self._SetInputValue("단위구분", unit)
        self.investor = {'ant': [], 'foreigner': [], 'agency': [], 'tusin': [], 'ocorporation':[], 'finvestment': [], 'date': []}    #초기화

        self._CommRqData("opt10060_req", "opt10060", "0")

    def _get_opt10060(self, tr_name, recode_name, index):
        n = self.dynamicCall("GetRepeatCnt(QString, QString)", tr_name, recode_name)

        for n in range(n):
            ant = self._GetCommData(tr_name, recode_name, n, "개인투자자")
            foreigner = self._GetCommData(tr_name, recode_name, n, "외국인투자자")
            agency = self._GetCommData(tr_name, recode_name, n, "기관계")
            tusin = self._GetCommData(tr_name, recode_name, n, "투신")
            finvestment = self._GetCommData(tr_name, recode_name, n, "금융투자")
            ocorporation = self._GetCommData(tr_name, recode_name, n, "기타금융")
            date = self._GetCommData(tr_name, recode_name, n, "일자")

            self.investor['ant'].insert(0, self.erase_strip(ant))
            self.investor['foreigner'].insert(0, self.erase_strip(foreigner))
            self.investor['agency'].insert(0, self.erase_strip(agency))
            self.investor['tusin'].insert(0, self.erase_strip(tusin))
            self.investor['ocorporation'].insert(0, self.erase_strip(ocorporation))
            self.investor['finvestment'].insert(0, self.erase_strip(finvestment))
            self.investor['date'].insert(0, self.erase_strip(date))

        self.investor = DataFrame(self.investor)

    #opt10080 분봉차트 조회 요청
    def _set_opt10080(self, stock_code, minute):
        self._SetInputValue("종목코드", stock_code)
        self._SetInputValue("틱범위", minute)
        self._SetInputValue("수정주가구분", 0)

        self.minOhlc = {'open': [], 'high': [], 'low': [], 'close': [], 'volume': [], 'date': []}  # 초기화
        #데이터 전송
        self._CommRqData("opt10080_req", "opt10080", "0")

    def _get_opt10080(self, tr_name, recode_name, index):
        n = self.dynamicCall("GetRepeatCnt(QString, QString)", tr_name, recode_name)

        for n in range(n):
            open = self._GetCommData(tr_name, recode_name, n, "시가")
            close = self._GetCommData(tr_name, recode_name, n, "현재가")
            high = self._GetCommData(tr_name, recode_name, n, "고가")
            low = self._GetCommData(tr_name, recode_name, n, "저가")
            date = self._GetCommData(tr_name, recode_name, n, "체결시간")
            volume = self._GetCommData(tr_name, recode_name, n, "거래량")

            self.minOhlc['open'].insert(0, abs(self.erase_strip(open)))
            self.minOhlc['close'].insert(0, abs(self.erase_strip(close)))
            self.minOhlc['high'].insert(0, abs(self.erase_strip(high)))
            self.minOhlc['low'].insert(0, abs(self.erase_strip(low)))
            self.minOhlc['date'].insert(0, abs(self.erase_strip(date)))
            self.minOhlc['volume'].insert(0, abs(self.erase_strip(volume)))

        self.minOhlc = DataFrame(self.minOhlc)

    #opt10081 일봉차트 조회 요청
    def _set_opt10081(self, stock_code, date, prevNext):
        self._SetInputValue("종목코드", stock_code)
        self._SetInputValue("기준일자", date)
        self._SetInputValue("수정주가구분", 0)

        self.ohlc = {'open': [], 'high': [], 'low': [], 'close': [], 'volume': [], 'date': []}  # 초기화

        #데이터 전송
        self._CommRqData("opt10081_req", "opt10081", prevNext)

    def _get_opt10081(self, tr_name, recode_name, prevNext):
        n = self.dynamicCall("GetRepeatCnt(QString, QString)", tr_name, recode_name)

        for i in range(n):
            open = self._GetCommData(tr_name, recode_name, i, "시가")
            close = self._GetCommData(tr_name, recode_name, i, "현재가")
            high = self._GetCommData(tr_name, recode_name, i, "고가")
            low = self._GetCommData(tr_name, recode_name, i, "저가")
            date = self._GetCommData(tr_name, recode_name, i, "일자")
            volume = self._GetCommData(tr_name, recode_name, i, "거래량")

            self.ohlc['open'].insert(0, (self.erase_strip(open)))
            self.ohlc['close'].insert(0, self.erase_strip(close))
            self.ohlc['high'].insert(0, self.erase_strip(high))
            self.ohlc['low'].insert(0, self.erase_strip(low))
            self.ohlc['date'].insert(0, self.erase_strip(date))
            self.ohlc['volume'].insert(0, self.erase_strip(volume))


        self.ohlc = DataFrame(self.ohlc)




    #opt10081 주봉차트 조회 요청
    def _set_opt10082(self, stock_code, date, endDate):
        self._SetInputValue("종목코드", stock_code)
        self._SetInputValue("기준일자", date)
        self._SetInputValue("끝일자", endDate)
        self._SetInputValue("수정주가구분", 0)

        self.week_ohlc = {'open': [], 'high': [], 'low': [], 'close': [], 'volume': [], 'date': []}  # 초기화
        #데이터 전송
        self._CommRqData("opt10082_req", "opt10082", "0")

    def _get_opt10082(self, tr_name, recode_name, index):
        n = self.dynamicCall("GetRepeatCnt(QString, QString)", tr_name, recode_name)

        for n in range(n):
            open = self._GetCommData(tr_name, recode_name, n, "시가")
            close = self._GetCommData(tr_name, recode_name, n, "현재가")
            high = self._GetCommData(tr_name, recode_name, n, "고가")
            low = self._GetCommData(tr_name, recode_name, n, "저가")
            date = self._GetCommData(tr_name, recode_name, n, "일자")
            volume = self._GetCommData(tr_name, recode_name, n, "거래량")


            self.week_ohlc['open'].insert(0, (self.erase_strip(open)))
            self.week_ohlc['close'].insert(0, self.erase_strip(close))
            self.week_ohlc['high'].insert(0, self.erase_strip(high))
            self.week_ohlc['low'].insert(0, self.erase_strip(low))
            self.week_ohlc['date'].insert(0, self.erase_strip(date))
            self.week_ohlc['volume'].insert(0, self.erase_strip(volume))

        self.week_ohlc = DataFrame(self.week_ohlc)


    def stringToNum(self, target):
        target = target.strip()

        if target[0] == '+':
            target = float(target[1: len(target)])
        elif target[0] == '-':
            target = float(target[1: len(target)]) * -1
        else:
            target = self.erase_strip(target)

        return target

    def erase_strip(self, target):
        return int(target.strip())








