import datetime as dt
from matplotlib import style
import pandas_datareader.data as web
import backtrader as bt

from src.strategies.beginner import sma_plot, TestStrategy, TestStrategy1, MAVGStrategy
from src.strategies.crossover import GoldenCrossStrategy


# 1.creating pandas dataframe object from web reader
style.use('ggplot')
start = dt.datetime(2017, 1, 1)
end = dt.datetime.now()
df = web.DataReader('AAPL', 'yahoo', start, end) # [EDIT]

# 2.reordering dataframe columns, and converting it into CSV for backtrader cerebro
cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
df1 = df.reindex(columns=cols)
print(df1)
df1.to_csv("aapl.csv") # [EDIT]

# 3.attaching csv and strategy to backtrader cerebro
cerebro = bt.Cerebro()
data = bt.feeds.YahooFinanceCSVData(dataname='aapl.csv') # [EDIT]
cerebro.adddata(data)
cerebro.addstrategy(GoldenCrossStrategy) # [EDIT]
cerebro.addsizer(bt.sizers.FixedSize, stake=100)

# 4.
cerebro.broker.set_cash(100000)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()

# sma_plot(df, 50, 200)
