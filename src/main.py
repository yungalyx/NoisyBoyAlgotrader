import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import mplfinance as mpf
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import backtrader as bt

from src.strategy import sma_plot, TestStrategy

# 1.creating pandas dataframe object from web reader
style.use('ggplot')
start = dt.datetime(2017, 1, 1)
end = dt.datetime.now()
df = web.DataReader('GOOGL', 'yahoo', start, end)

# 2.reordering dataframe columns, and converting it into CSV for backtrader cerebro
cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
df1 = df.reindex(columns=cols)
print(df1)
df1.to_csv("goog.csv")

# 3.attaching csv and strategy to backtrader cerebro
cerebro = bt.Cerebro()
data = bt.feeds.YahooFinanceCSVData(dataname='goog.csv')
cerebro.adddata(data)
cerebro.addstrategy(TestStrategy)

# 4.
cerebro.broker.set_cash(100000)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

sma_plot(df, 50, 200)
