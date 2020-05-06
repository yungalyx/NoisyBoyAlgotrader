import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import dash

SECRET_KEY = 'MT6ZPUdqChaXPF/fdz/P7zCUihYDNlnvSbhF8ZeZ'
API_KEY = 'PKAEF0MF359GKY0XS5SK'
ENDPOINT_URL = 'https://paper-api.alpaca.markets'
TIINGO_KEY = '3b766e3ad439feb379b9b2cdd0e677761ae72842'

response = {'service': 'iex',
            'messageType': 'A',
            'data': ['T', '2020-04-29T10:35:15.491012812-04:00', 1588170915491012812, 'spy',
                     None, None, None, None, None, 292.27, 100, None, 0, 0, 0, 0]}

df = pd.DataFrame(columns=['Date', 'open', 'high', 'low', 'close'])
df = df.append({'Date': '05/02/2020 1:27', 'open': 500, 'high': 501, 'low': 499, 'close': 497}, ignore_index=True)
df = df.append({'Date': '05/02/2020 1:28', 'open': 299, 'high': 303, 'low': 296, 'close': 303}, ignore_index=True)
df = df.append({'Date': '05/02/2020 1:29', 'open': 103, 'high': 106, 'low': 102, 'close': 107}, ignore_index=True)

print(df)


print(len(df))
print(len(df) - 1)

'''fig = go.Figure(data=go.Ohlc(x=df['Date'],
                             open=df['open'],
                             high=df['high'],
                             low=df['low'],
                             close=df['close']))
fig.show()'''
print(df.at[len(df) - 1, 'close'])

df.at[len(df) - 1, 'close'] = 500
