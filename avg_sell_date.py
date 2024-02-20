import requests
import ipdb
import numpy as np
from sklearn.linear_model import LinearRegression
import json
import csv
import matplotlib.pyplot as plt
import sys

# jsdt = json.load('./hsiStockList.json')
with open('./hsiStockList.json', 'r', encoding='utf-8') as file:
    jsdt = json.load(file)
    symbols = [item['symbol'] for item in jsdt]
print(symbols)
symbols=['9888.HK',
'1928.HK',
'2899.HK',
'1088.HK',
'0316.HK',
'0883.HK',
'6862.HK',
'0981.HK',
'0005.HK',
'0857.HK',
]
evaluate="strategy" #strategy/non-strategy
profit_rate=0.05

url = 'https://hi.comp.polyu.edu.hk/backend/stocks/query'

# "symbol": "0005.HK",
# "high": 47.15,
# "low": 46.65,
# "open": 47,
# "close": 46.85,
# "adjClose": 44.888348,
# "vloume": 6711558,
# "date": "2022-01-03T00:00:00.000Z"
sell_gap=[]
for syb in symbols:

    # syb="0316.HK"
    params={

    'fromDate': '2021-08-23',

    'toDate': '2023-09-23',

    'symbol': syb,

    'order?': 'ASC',

    }
    # ipdb.set_trace()
    response = requests.get(url,params=params)
    def cal_argument(daily_close,p_gain,p_loss):
        buy_signal = False
        sell_signal = False
        # calculate down market
        tdaily_close = np.array(daily_close[-30:])
        date_ct = [i for i in range(tdaily_close.shape[0])]
        date_ct = np.array(date_ct)
        model = LinearRegression()
        model.fit(tdaily_close, date_ct)
        slope = model.coef_[0]

        # Cal RSI
        tp_gain = np.array(p_gain)
        tp_loss = np.array(p_loss)
        ag = tp_gain[-14:].mean()
        al = tp_loss[-14:].mean()
        RS = ag / al
        RSI = 100 - (100 / (1 + RS))

        return slope,RSI

      #strategy/ non-strategy


    if response.status_code == 200:
        data = response.json()
        daily_close=[]
        # date_ct=[]
        p_gain=[]
        p_loss=[]
        prev_close=0
        prev_RSI=0
        ct=0
        INITIAL_BALANCE=1000000
        balance=INITIAL_BALANCE
        holding_price = 1
        holding_volume=0

        # lists for figure
        today_close_values = []
        balance_values = []
        balance_days = []

        buy_value = []
        buy_dates = []  # buy date
        sell_dates = []  # sell date


        # buy_date=[]
        # sell_date=[]


        for item in data:
            ct+=1
            today_close=item["close"]
            today_close_values.append(today_close)
            if ct==1:
                p_gain.append(0)
                p_loss.append(0)
            else:
                if today_close>prev_close:
                    p_gain.append(today_close-prev_close)
                    p_loss.append(0)
                else:
                    p_gain.append(0)
                    p_loss.append(prev_close-today_close)



            # print(item)
            daily_close.append([today_close])
            # date_ct.append(ct)
            prev_close=today_close
            buy_signal=False
            sell_signal=False
            if ct>=61:
                slope,RSI=cal_argument(daily_close,p_gain,p_loss)

                # Trading per week
                if((ct-61)%7==0):
                    if evaluate =="strategy":
                        # print(holding_volume,holding_price,today_close)
                        if(slope<0 and RSI>prev_RSI and RSI>30):
                            buy_signal=True
                            buy_dates.append(ct)
                            buy_value.append(today_close)
                            sell_dates.append(-1)
                        elif(slope>=0 and RSI<=prev_RSI and RSI>30):
                            buy_signal=True
                            buy_dates.append(ct)
                            buy_value.append(today_close)
                            sell_dates.append(-1)

                        for i in range(len(buy_value)):
                            if((today_close-buy_value[i])/buy_value[i]>=profit_rate):
                                sell_dates[i]=ct
                    else:
                        buy_dates.append(ct)
                        buy_value.append(today_close)
                        sell_dates.append(-1)
                        for i in range(len(buy_value)):
                            if((today_close-buy_value[i])/buy_value[i]>=profit_rate):
                                sell_dates[i]=ct


                prev_RSI = RSI
        for i in range(len(sell_dates)):
            if sell_dates[i]==-1:
                sell_dates[i]=ct
        sell_dates=np.array(sell_dates)
        buy_dates=np.array(buy_dates)
        # print((sell_dates-buy_dates).mean())
        sell_gap.append((sell_dates-buy_dates).mean())
        print(sell_gap)
        # ipdb.set_trace()
                # print(f"Date: {item['date'][:10]}, day {ct}, if down market for 1 month:{slope < 0}, RSI:{RSI}, RSI higher than prev RIS:{RSI > prev_RSI}")
        # print(holding_volume,today_close)
        # print(f"Trading ends, Date: {item['date'][:10]}, day {ct}, balance:{balance + holding_volume * today_close}, initial balance={INITIAL_BALANCE}, profit rate={(balance + holding_volume * today_close-INITIAL_BALANCE)/INITIAL_BALANCE}")

        # with open("result_60_19_21.csv", "a+") as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow([syb,balance + holding_volume * today_close, (balance + holding_volume * today_close-INITIAL_BALANCE)/INITIAL_BALANCE])
    else:

        print('request lose:', response.status_code)
sell_gap=np.array(sell_gap)
print(sell_gap)
print(sell_gap.mean(),evaluate,"profit rate=",profit_rate)