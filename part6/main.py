from pytickersymbols import PyTickerSymbols
import yfinance as yf
import datetime
import pickle
import os
import pandas as pd
from Portfolio import Portfolio
from kpi import print_strategy_summary

# get ticker names (can use CSV file)
stock_data = PyTickerSymbols()
sp500_tickers = [stock["symbol"] for stock in stock_data.get_stocks_by_index('S&P 500')]
medium_tickers = list(pd.read_csv("medium_tickers.csv")["Ticker"])
# cryptocurrency data
'''
btc = yf.download("BTC-USD",
                           start = datetime.datetime.today() - datetime.timedelta(3 * 365),
                           end = datetime.datetime.today(),
                           interval = "1mo",
                           progress = False)'''
    
# cryptocompare
'''import cryptocompare
cryptocompare.get_price('BTC', currency="USD")'''

# load data 
def get_ohlcv(name, tickers, start, end, interval, save = True):
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
        
    if save:
        with open(name, "wb") as f:
            pickle.dump(ohlcv, f)
        
    return ohlcv
    
def test_ma_strat(ticker, start, end, periods):
    # load data
    stock = get_ohlcv("", [ticker], start, end, "1mo", save = False)[ticker]
    
    # generate moving average
    stock["MA"] = stock["Adj Close"].ewm(span = 6, min_periods = 6).mean()
    
    # set up portfolio
    
    # strategy portfolio
    PORTFOLIO = Portfolio()
    values = []
    
    # buy and hold portfolio
    SIMPLE_PORTFOLIO = Portfolio()
    simple_values = []
    
    # execute strategy
    for i in range(len(stock)):
        if i == 0:
            SIMPLE_PORTFOLIO.add_position(ticker, stock["Adj Close"][i], SIMPLE_PORTFOLIO.get_cash())
        
        # update prices
        PORTFOLIO.advance(ticker, stock["Adj Close"][i])
        SIMPLE_PORTFOLIO.advance(ticker, stock["Adj Close"][i])
        
        # determine actions
        # is trend bearish?
        if stock["Adj Close"][i] < stock["MA"][i]:
            if PORTFOLIO.have_position(ticker):
                PORTFOLIO.close_position(ticker, stock["Adj Close"][i])
        else:
            # we are bullish!
            if PORTFOLIO.get_cash() > 0:
                PORTFOLIO.add_position(ticker, stock["Adj Close"][i], PORTFOLIO.get_cash())
                
        # update historical values
        values.append(PORTFOLIO.get_total_value())
        simple_values.append(SIMPLE_PORTFOLIO.get_total_value())
    
    # analyze results
    # simple portfolio
    d = {'Date': list(stock.index), 'value': simple_values}
    df_simple = pd.DataFrame(data = d)
    df_simple.set_index("Date", inplace = True)
    
    # quant portfolio
    d = {'Date': list(stock.index), 'value': values}
    df = pd.DataFrame(data = d)
    df.set_index("Date", inplace = True)
    
    print_strategy_summary("Simple", periods, df_simple, price_col_name = "value")
    print()
    print_strategy_summary("Quant", periods, df, price_col_name = "value") 
test_ma_strat("SPY", datetime.datetime.today() - datetime.timedelta(15 * 365), datetime.datetime.today(), 12)

    
