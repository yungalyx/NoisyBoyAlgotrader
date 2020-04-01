import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import mplfinance as mpf
import matplotlib.dates as mdates
import pandas as pd
import backtrader as bt
import backtrader.indicators as btind
import math


class AllocationStrategy(bt.Strategy):
    params = (("BBandsPeriod", 20), ("Order_Percentage", 0.08), ("Ticker", "NFLX"))

    def log(self):
        pass

    def __init__(self):
        self.bbands = btind.BollingerBands(self.data, period=self.params.BBandsPeriod)
        self.order = None

    def next(self):
        # if i have an order, then don't worry
        # if self.order:
        #    return

        # if i'm not in a position
        #if not self.position:
            cash_on_hand = self.broker.get_cash()
            invest_amt = cash_on_hand * self.params.Order_Percentage
            # if today's price opened is below bband,
            if self.datas[0].close < self.bbands.lines.bot[0]:

                # and yesterday's close was below bband
                if self.datas[-1].close < self.bbands.lines.bot[-1]:
                    self.size = math.floor(invest_amt / self.data.close)
                    print("Buy {} shares of {} at {}".format(self.size, self.params.Ticker, self.data.close[0]))
                    self.buy(size=self.size)

      #  else:
            if self.datas[0].close > self.bbands.lines.top[0]:
                if self.datas[-1].close > self.bbands.lines.top[-1]:
                    print("Sell {} shares of {} at {}".format(self.position.size, self.params.Ticker, self.data.close[0]))
                    self.close()
                    # self.order = None




