from Position import Position

class Portfolio:
    def __init__(self, cash = 1000):
        self.portfolio = {}
        self.cash = cash

    def add_position(self, ticker, original_price, value, long = True):
        if ticker in self.portfolio:
            print("ERROR - position already exists")
            return
        if not self.can_afford(value):
            print("ERROR - cannot afford")
            return
        self.cash -= value
        self.portfolio[ticker] = Position(ticker, original_price, value, long = long)
        
    def have_position(self, ticker):
        return ticker in self.portfolio
    
    def close_position(self, ticker, price):
        if ticker not in self.portfolio:
            return 0
        val = self.portfolio[ticker].close(price)
        del self.portfolio[ticker]
        self.cash += val
        return val
    
    def advance(self, ticker, price):
        if ticker in self.portfolio:
            self.portfolio[ticker].advance(price)
            
    def get_cash(self):
        return self.cash

    def get_num_positions(self):
        return len(self.portfolio)
    
    def get_total_value(self):
        return sum([position.get_value() for position in self.portfolio.values()]) + self.cash
    
    def can_afford(self, cost):
        return self.cash >= cost
    
    def get_position(self, ticker):
        if ticker in self.portfolio:
            return self.portfolio[ticker]
        
    def get_positions(self):
        return list(self.portfolio.keys())
    
    def __str__(self):
        return "Portfolio of {} positions with total value of {} and tickers: {}".format(self.get_num_positions(), self.get_total_value(), self.get_positions())
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    