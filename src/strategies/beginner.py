import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import mplfinance as mpf
import matplotlib.dates as mdates
import pandas as pd
import backtrader as bt
import backtrader.indicators as btind


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

# buys a 2 day dip, holds 5 days and sell.
class TestStrategy1(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        # creating an order status
        self.order = None
        self.bar_executed = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED {}'.format(order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED {}'.format(order.executed.price))

            self.bar_executed = len(self)

        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close

                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
        else:
            if len(self) >= (self.bar_executed + 5):
                self.log('SELL ORDER CREATED {}'.format(self.dataclose[0]))
                # buy and sell orders are created at end of day, so trades aren't actualized until next day market open
                self.order = self.sell()

# buys if below mavg, sells if above
class MAVGStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.sma = btind.MovingAverageSimple(period=8)

    def next(self):
        if self.sma > self.data.close:
            self.log('BUY CREATE, %.2f' % self.data.close[0])
            print(self.sma[0] - self.data.close[0])  # Prints the difference in SMA and current price
            self.buy()

        elif self.sma < self.data.close:
            self.log('SELL ORDER CREATED {}'.format(self.data.close[0]))
            # buy and sell orders are created at end of day, so trades aren't actualized until next day market open
            self.sell()




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
