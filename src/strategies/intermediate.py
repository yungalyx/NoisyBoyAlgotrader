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
    params = (("BBandsPeriod", 20), ("Order_Percentage", 0.5))

    def log(self):
        pass

    def __init__(self):
        self.inds = dict()  # going to store indicators in dictionary for each stock ive added
        for i, d in enumerate(self.datas):
            self.inds[d] = btind.BollingerBands(d, period=self.params.BBandsPeriod)
            # self.Orders = none


    def next(self):
        cash_on_hand = self.broker.get_cash()
        invest_amt = cash_on_hand * self.params.Order_Percentage
        # if today's price opened is below bband,

        for i, d in enumerate(self.datas):  # i refers to index, d refers to data object it is attached to
            dn = d._name
            print(dn)

            # if close was below botlinger today and yesterday, enter trade
            if self.datas[i].close[0] < self.inds[d].lines.bot[0]:
                if self.datas[i].close[-1] < self.inds[d].lines.bot[-1]:
                    self.size = math.floor(invest_amt / self.data.close)
                    print("Buy {} shares of {} at {}".format(self.size, dn, self.data.close[0]))
                    self.buy(data=d, size=self.size)

            elif self.datas[i].close[0] > self.inds[d].lines.top[0]:
                if self.datas[i].close[-1] > self.inds[d].lines.top[-1]:
                    print(
                        "Sell {} shares of {} at {}".format(self.position.size, dn, self.data.close[0]))
                    self.close(data=d)
                    # self.order = None








        # if d[0].close < self.inds[d].bot[0]:

            # and yesterday's close was below bband
            '''
          
            if self.datas[-1].close < self.bbands.lines.bot[-1]:
                self.size = math.floor(invest_amt / self.data.close)
                print("Buy {} shares of {} at {}".format(self.size, self.params.Ticker, self.data.close[0]))
                self.buy(size=self.size)


        if self.datas[0].close > self.bbands.lines.top[0]:
            if self.datas[-1].close > self.bbands.lines.top[-1]:
                print("Sell {} shares of {} at {}".format(self.position.size, self.params.Ticker, self.data.close[0]))
                self.close()
                # self.order = None
  '''



