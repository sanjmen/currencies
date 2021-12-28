import pandas as pd

import ccxt

from django.conf import settings

class Broker:
    def __init__(self, exchange=settings.DEFAULT_EXCHANGE):
        self.client = getattr(ccxt, exchange)()

    def get_markets(self):
        return self.client.load_markets()

    def get_symbol_info(self, symbol):
        markets = self.get_markets()
        
        return markets[symbol]

    def get_klines(self, symbol, interval):
        # list of [ open_time, open, high, low, close, volume ]
        klines = self.client.fetch_ohlcv(symbol, interval)
        
        return klines
