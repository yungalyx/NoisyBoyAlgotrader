import datetime as dt
from matplotlib import style
import pandas_datareader.data as web
import backtrader as bt
import matplotlib.pyplot as plt
import pyfolio as pf

from src.strategies.beginner import sma_plot, TestStrategy, TestStrategy1, MAVGStrategy
from src.strategies.crossover import GoldenCrossStrategy
from src.strategies.intermediate import AllocationStrategy

# 1.creating pandas dataframe object from web reader
style.use('ggplot')
start = dt.datetime(2017, 1, 1)
# end = dt.datetime(2020, 1, 1)
end = dt.datetime.now()

ticker_list = ['PG', 'JCP', 'TSLA', 'RACE'] # Nflx, zm, wm, lulu, LMT,

cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

# init cerebro
cerebro = bt.Cerebro()

# converting ticker to web data to csv and inserting into cerebro
for i in ticker_list:
    print(i)
    df = web.DataReader(i, 'yahoo', start, end)
    df = df.reindex(columns=cols)
    df.to_csv('%s.csv' % i)  # might need to two line this
    data = bt.feeds.YahooFinanceCSVData(dataname='%s.csv' % i)  # along w this
    cerebro.adddata(data, name=i)


df3= web.DataReader('PG', 'yahoo', start, end)
df3 = df3.reindex(columns=['High', 'Close', 'Adj Close'])
print(df3.tail(5))

cerebro.addstrategy(AllocationStrategy)  # [EDIT]
# cerebro.addsizer(bt.sizers.FixedSize, stake=10)

# 4.
cerebro.broker.set_cash(100000)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
strats = cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()



# sma_plot(df, 50, 200)
