import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import mplfinance as mpf
import matplotlib.dates as mdates
import pandas as pd
import backtrader as bt
import backtrader.indicators as btind
import math

class GoldenCrossStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        pass

    def __init__(self):
        self.mavg200 = btind.MovingAverageSimple(self.data.close, period=200)
        self.mavg50 = btind.MovingAverageSimple(self.data.close, period=50)
        self.crossover = btind.CrossOver(self.mavg50, self.mavg200)
        self.size = 0
        self.order_percentage = 0.5

    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                amount_to_invest = self.order_percentage * self.broker.cash
                self.size = math.floor(amount_to_invest / self.data.close)
                print("Buy {} shares of {} at {}".format(self.size, 'tsla', self.data.close[0]))
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.crossover < 0:
                print("Sell {} shares of {} at {}".format(self.size, 'tsla', self.data.close[0]))
                self.close()







