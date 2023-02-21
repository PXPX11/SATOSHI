import requests
import pandas as pd
import datetime
import numpy as np


def gen_calendar():
    this_year = datetime.datetime.now()
    years = range(this_year.year, 2009, -1)  # Fugle提供的資料從2010年
    begin = [int(str(y) + '0101') for y in years]
    end = [int(str(y) + '1231') for y in years]
    calendar = pd.DataFrame({'begin': begin,
                             'end': end})
    calendar['begin'] = pd.to_datetime(calendar['begin'], format='%Y%m%d')
    calendar['end'] = pd.to_datetime(calendar['end'], format='%Y%m%d')
    calendar[['begin', 'end']] = calendar[['begin', 'end']].astype('str')
    return calendar


def get_hist_data(symbol):
    result = []
    calendar = gen_calendar()

    for j in range(len(calendar)):
        cur_begin = calendar.loc[j, 'begin']
        cur_end = calendar.loc[j, 'end']

        data_link = f'https://api.fugle.tw/marketdata/v0.3/candles?symbolId={symbol}&apiToken=demo&from={cur_begin}&to={cur_end}&fields=open,high,low,close,volume,turnover,change'
        resp = requests.get(url=data_link)
        data = resp.json()

        candles = data['data']
        result += candles

    result = pd.DataFrame.from_dict(result)
    result['symbol'] = symbol

    return result


if __name__ == '__main__':
    # 全部股票歷史資料
    # data = get_hist_data()
    # 單一個股歷史資料 - 2330台積電
    data = get_hist_data(symbols=['2330'])
