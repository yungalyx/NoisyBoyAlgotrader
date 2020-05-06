import requests, json, websocket
import alpaca_trade_api as tradeapi
import dateutil.parser
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
from src.setup import TIINGO_KEY

TICKER = ['AAPL', 'RACE', 'TSLA']

# for processing intraday data stream
minutes_processed = {}  # dictionary
minute_candlesticks = pd.DataFrame(columns=['minute', 'open', 'high', 'low', 'close'])
current_tick = None  # tracking current tick
previous_tick = None


def on_open(ws):
    print('=== Opened Connection ===')
    # set up graphing
    # set_up_graph()

    # authenticate
    auth_data = {
        'eventName': 'subscribe',
        'authorization': TIINGO_KEY,
        'eventData': {
            'thresholdLevel': 5,
            'tickers': ['spy']
        }
    }
    ws.send(json.dumps(auth_data))

    # do not listen to the IDE... this method is NOT static

def on_message(ws, message):
    global current_tick, previous_tick, minute_candlesticks
    previous_tick = current_tick
    current_tick = json.loads(message)

    if current_tick['messageType'] == 'A' and current_tick['data'][9] is not None:
        print('==+ RECEIVED TICK +==')
        tick_price = current_tick['data'][9]
        tick_datetime_obj = dateutil.parser.parse(current_tick['data'][1])
        tick_dt = tick_datetime_obj.strftime('%m/%d/%Y %H:%M')  # minute is smallest factor of change
        print('{} @ {}'.format(tick_dt, tick_price))

        # checking for new minute
        if tick_dt not in minutes_processed:
            print('++++++ STARTING NEW CANDLE STICK ++++++')
            minutes_processed[tick_dt] = True
            print(minutes_processed)  # prints

            if len(minute_candlesticks) >= 1:
                minute_candlesticks.at[len(minute_candlesticks) - 1, 'close'] = tick_price

            # try using tick_dt if it doesnt look as nice
            minute_candlesticks = minute_candlesticks.append({
                'minute': tick_dt, 'open': tick_price, 'high': tick_price, 'low': tick_price, 'close': None},
                ignore_index=True)

        print(minute_candlesticks)

        # this works.
        if len(minute_candlesticks) > 0:
            if tick_price > minute_candlesticks.at[len(minute_candlesticks) - 1, 'high']:
                minute_candlesticks.at[len(minute_candlesticks) - 1, 'high'] = tick_price
            if current_tick < minute_candlesticks.at[len(minute_candlesticks) - 1, 'low']:
                minute_candlesticks.at[len(minute_candlesticks) - 1, 'high'] = tick_price

            print(minute_candlesticks)

    else:
        print(current_tick)


socket = 'wss://api.tiingo.com/iex'
ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
ws.run_forever()
