from pytickersymbols import PyTickerSymbols
import yfinance as yf
import datetime

# get ticker names (can use CSV file)
stock_data = PyTickerSymbols()
sp500_tickers = [stock["symbol"] for stock in stock_data.get_stocks_by_index('S&P 500')]

# load data
ohlcv = {}
for ticker in sp500_tickers[:10]:
    # get the data
    stock = yf.download(ticker,
                       start = datetime.datetime.today() - datetime.timedelta(3 * 365),
                       end = datetime.datetime.today(),
                       interval = "1mo",
                       progress = False)
    
    # drop na rows
    stock.dropna(inplace = True)
    
    if len(stock) == 0: continue
    
    # save to dictionary by ticker
    ohlcv[ticker] = stock
   
