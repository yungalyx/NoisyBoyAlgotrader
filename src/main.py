import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import mplfinance as mpf
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')
start = dt.datetime(2019, 2, 18) #my birthday!
end = dt.datetime.now()

df = web.DataReader('TSLA', 'yahoo', start, end) # this is dataframe!

'''
print("IPO:")
print(df.head())
print("RECENT:")
print(df.tail())
'''

#scrape_sp500_tickers()
#get_data_from_yahoo()



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

#4. resampling daily data
df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

df_ohlc.reset_index(inplace=True)

df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

print(df_ohlc.head())
#10D, 10M, 6M, #.mean(), .sum(), .rolling(), .ohlc()

print("HELLO")
mpf.plot(df, type='candle', style='yahoo', mav=(30, 60), volume=True)


#3. plotting
ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()


ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])

#plt.show()




