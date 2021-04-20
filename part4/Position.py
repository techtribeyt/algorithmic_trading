# use this to keep track of single open position

class Position:
    def __init__(self, ticker, original_price, value, long = True):
        # value: dollar amount of purchase
        # long = betting price will appreciate, short = betting price will drop
        
        self.ticker = ticker
        self.original_price = original_price
        self.original_value = value
        self.value = value
        self.price = original_price
        self.long = long
        
    def get_value(self):
        return self.value
    
    def update_value(self):
        if self.long:
            self.value = self.original_value * self.price / self.original_price
        else:
            self.value = self.original_value * self.original_price / self.price
    
    def close(self, price):
        self.price = price
        self.update_value()
        return self.value
    
    def advance(self, price):
        self.price = price
        self.update_value()
        
    def __str__(self):
        return "{}: original value: {}, current value: {}. Last price: {}".format(self.ticker, self.original_value, self.value, self.price)
        