from pytickersymbols import PyTickerSymbols
import yfinance as yf
import datetime
import pickle
import os
import pandas as pd

# get ticker names (can use CSV file)
stock_data = PyTickerSymbols()
sp500_tickers = [stock["symbol"] for stock in stock_data.get_stocks_by_index('S&P 500')]
medium_tickers = list(pd.read_csv("medium_tickers.csv")["Ticker"])

# load data 
def get_ohlcv(name, tickers, start, end, interval):
    # if we already have a save with this name
    if os.path.exists(name):
        with open(name, "rb") as f:
            return pickle.load(f)
        
    ohlcv = {}
    for ticker in tickers:
        # get the data
        stock = yf.download(ticker,
                           start = start,
                           end = end,
                           interval = interval,
                           progress = False)
        
        # drop na rows
        stock.dropna(inplace = True)
        
        if len(stock) == 0: continue
        
        # save to dictionary by ticker
        ohlcv[ticker] = stock
        
    with open(name, "wb") as f:
        pickle.dump(ohlcv, f)
        
    return ohlcv
    