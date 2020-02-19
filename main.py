import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')
start = dt.datetime(2000, 2, 18) #my birthday!
end = dt.datetime(2020, 2, 18) #today!! wow 20 years

df = web.DataReader('TSLA', 'yahoo', start, end) # this is dataframe!
print("IPO:")
print(df.head())
print("RECENT:")
print(df.tail())
#df.plot()
'''
 df.to_csv('tsla')
 df = pd.read_csv('tsla', parse_dates=True, index_col=0)
 plotting specific colm's: df['Adj Close'].plot()
 printing value of spec. cols: print(df[['Open', 'Close']].head())

Adding additional Columns!
df.dropna(inplace=True), basically disregards all days where values aren't available 

Subplotting!
'''

df['100ma'] = df['Adj Close'].rolling(window=100).mean()

ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)

ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])

plt.show()


