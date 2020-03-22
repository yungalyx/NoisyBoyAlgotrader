import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import mplfinance as mpf
import matplotlib.dates as mdates
import pandas as pd
import backtrader as bt


# given a stock df
# return plot for sma crossover
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        if self.dataclose[0] < self.dataclose[-1]:
            # current close less than previous close

            if self.dataclose[-1] < self.dataclose[-2]:
                # previous close less than the previous close

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()


def trading_signals(position):
    grace = position.replace(0, np.nan)
    return grace

# takes in a yahoo webReader dateFrame object
def sma_plot(df, short, long):
    df['long_ma'] = df['Close'].rolling(long).mean()
    df['short_ma'] = df['Close'].rolling(short).mean()
    df['signals'] = 0.0
    df['signals'] = np.where(df['short_ma'] > df['long_ma'], 1.0, 0.0)
    df['pos'] = df['signals'].diff()

    signal = trading_signals(df['pos'])

    # making trading signal subplot
    adp = mpf.make_addplot(signal, scatter=True, marker='^')

    # adding our own scatter plot onto the mpf plot
    mpf.plot(df, addplot=adp, type='candle', style='yahoo', mav=(short, long), volume=True)

    print(df[['short_ma', 'long_ma', 'Close', 'signals', 'pos']].tail(10))
