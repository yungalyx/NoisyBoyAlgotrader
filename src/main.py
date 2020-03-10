import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import mplfinance as mpf
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
import numpy as np

style.use('ggplot')
start = dt.datetime(2019, 2, 18)  # my birthday!
# end = dt.datetime.now()
end = dt.datetime(2020, 1, 7)
df = web.DataReader('WM', 'yahoo', start, end)  # this is dataframe!

'''
print("IPO:")
print(df.head())
print("RECENT:")
print(df.tail())
'''

# scrape_sp500_tickers()
# get_data_from_yahoo()


# df.plot()
'''
 df.to_csv('tsla')
 df = pd.read_csv('tsla', parse_dates=True, index_col=0)
 plotting specific colm's: df['Adj Close'].plot()
 printing value of spec. cols: print(df[['Open', 'Close']].head())

Adding additional Columns!
df.dropna(inplace=True), basically disregards all days where values aren't available 

Subplotting!
'''


# 4. resampling daily data


# df_ohlc = df['Adj Close'].resample('10D').ohlc()
# df_volume = df['Volume'].resample('10D').sum()
# df_ohlc.reset_index(inplace=True)

# df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
# 10D, 10M, 6M, #.mean(), .sum(), .rolling(), .ohlc()


def trading_signals(position):
    grace = position.replace(0, np.nan)
    return grace


# altering dateframe object, notice that mpf.plot and df are two seperate libraries!!
df['30ma'] = df['Close'].rolling(30).mean()
df['60ma'] = df['Close'].rolling(60).mean()
df['signals'] = 0.0
df['signals'] = np.where(df['30ma'] > df['60ma'], 1.0, 0.0)
df['pos'] = df['signals'].diff()

# creating a signal dataseries where only correct values are plotted.
signal = trading_signals(df['pos'])

# creating a scatter plot
adp = mpf.make_addplot(signal, scatter=True)

# adding our own scatter plot onto the mpf plot
mpf.plot(df, addplot=adp, type='candle', style='yahoo', mav=(30, 60), volume=True)

print(df[['30ma', '60ma', 'Close', 'signals', 'pos']].tail(10))
'''
if df.tail['30ma'] > df.tail['60ma']:
     print("30 day ma is greater than 60 day ma")
'''

# 3. plotting
'''
ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()


ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['80ma'])
ax2.bar(df.index, df['Volume'])

plt.show()
'''
