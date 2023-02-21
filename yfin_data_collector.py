import requests
import pandas as pd
import datetime
import yfinance as yf


def get_hist_data(symbols):
    result = {}

    for i, symbol in enumerate(symbols):
        stock = yf.Ticker(symbol)
        symbol_result = stock.history(period='max')

        result[symbol] = symbol_result

    return result


if __name__ == '__main__':
    data = get_hist_data(symbols=['^GSPC'])
