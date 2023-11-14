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


url = 'https://hi.comp.polyu.edu.hk/backend/stocks/query'

# "symbol": "0005.HK",
# "high": 47.15,
# "low": 46.65,
# "open": 47,
# "close": 46.85,
# "adjClose": 44.888348,
# "vloume": 6711558,
# "date": "2022-01-03T00:00:00.000Z"

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
    # 处理响应
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

        # 初始化列表来存储数据点
        today_close_values = []
        balance_values = []
        balance_days = []
        buy_dates = []  # 买入的日期
        sell_dates = []  # 卖出的日期

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
                    sold=0
                    # print(holding_volume,holding_price,today_close)
                    if(slope<0 and RSI>prev_RSI and RSI>30):
                        buy_signal=True

                    if((today_close-holding_price)/holding_price>=0.05):
                        sell_signal=True
                    #sell
                    if(sell_signal):
                        if holding_volume!=0:
                            balance+=holding_volume*today_close
                            sold=1
                            print(f"Date: {item['date'][:10]},today close:{today_close}, balance:{balance}, sell obtain: {holding_volume*today_close}")
                            holding_volume = 0
                            sell_dates.append(ct)
                    if(buy_signal and sold==0):
                        buy_volume=balance//today_close
                        holding_volume+=buy_volume
                        balance-=buy_volume*today_close
                        #buy
                        if(buy_volume!=0):
                            holding_price = today_close
                            print(f"Date: {item['date'][:10]},today close:{today_close}, balance:{balance}, buy expenditure: {buy_volume * today_close}")
                            buy_dates.append(ct)
                    balance_values.append(balance + holding_volume * today_close)
                    balance_days.append(ct)  # 记录余额记录的时间点
                prev_RSI = RSI
                # print(f"Date: {item['date'][:10]}, day {ct}, if down market for 1 month:{slope < 0}, RSI:{RSI}, RSI higher than prev RIS:{RSI > prev_RSI}")
        # print(holding_volume,today_close)
        print(f"Trading ends, Date: {item['date'][:10]}, day {ct}, balance:{balance + holding_volume * today_close}, initial balance={INITIAL_BALANCE}, profit rate={(balance + holding_volume * today_close-INITIAL_BALANCE)/INITIAL_BALANCE}")

        #draw figure
        fig, ax1 = plt.subplots()
        color = 'tab:red'
        ax1.set_xlabel('Days')
        ax1.set_ylabel('Balance', color=color)
        ax1.plot(balance_days, balance_values, color=color,alpha=0.7)
        ax1.tick_params(axis='y', labelcolor=color)


        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Today Close', color=color)
        ax2.plot(today_close_values, color=color,alpha=0.7)
        ax2.tick_params(axis='y', labelcolor=color)


        ax2.scatter(buy_dates, [today_close_values[i] for i in buy_dates], color='black', marker='^', label='Buy')
        ax2.scatter(sell_dates, [today_close_values[i] for i in sell_dates], color='black', marker='v', label='Sell')
        ax2.legend()
        plt.title(f'Stock Trading Strategy Performance-{syb}')
        plt.savefig(f'./result/plot{syb}.png')
        # sys.exit()
        with open("result_60.csv", "a+") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([syb,balance + holding_volume * today_close, (balance + holding_volume * today_close-INITIAL_BALANCE)/INITIAL_BALANCE])
    else:

        print('请求失败：', response.status_code)