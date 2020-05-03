import requests, json, websocket
import alpaca_trade_api as tradeapi
import dateutil.parser
import plotly.graph_objects as go
import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
from src.setup import ENDPOINT_URL, SECRET_KEY, API_KEY, TIINGO_KEY

ACCOUNT_URL = '{}/v2/account'.format(ENDPOINT_URL)
ORDER_URL = '{}/v2/orders'.format(ENDPOINT_URL)
DATA_URL = 'https://data.alpaca.markets/v1'
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
TICKER = ['AAPL', 'RACE', 'TSLA']

# for processing intraday data stream
minutes_processed = {}  # dictionary
minute_candlesticks = pd.DataFrame(columns=['minute', 'open', 'high', 'low', 'close'])
current_tick = None  # tracking current tick
previous_tick = None


class PaperTradingBot:

    # this function not used until bot is deployed
    def __init__(self):
        self.alpaca = tradeapi.REST(API_KEY, SECRET_KEY, ENDPOINT_URL, api_version='v2')
        self.alpacadata = tradeapi.REST(API_KEY, SECRET_KEY, DATA_URL)

    def on_open(ws):
        print('=== Opened Connection ===')
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
        global current_tick, previous_tick
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

                if len(minute_candlesticks) > 0:
                    minute_candlesticks[len(minute_candlesticks) - 1]['close'] = previous_tick['data'][9]

                # TODO: change this list into pandas object
                minute_candlesticks.append({
                    'minute': tick_dt,
                    'open': tick_price,
                    'high': tick_price,
                    'low': tick_price,
                    'close': None  # try using tick_dt if it doesnt look that nice
                }, ignore_index=True)

            print(minute_candlesticks)

            # might have issues accessing and changing pandas dateframe obj
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

    fig = go.Figure(data=go.Ohlc(x=minute_candlesticks['minute'],
                                 open=minute_candlesticks['open'],
                                 high=minute_candlesticks['high'],
                                 low=minute_candlesticks['low'],
                                 close=minute_candlesticks['close']))

    # or use fig.show()
    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    app.run_server(debug=True)




'''
bd = PaperTradingBot()
bd.run()
'''


# ======== DASHBOARD ==============


# everything below here is REST
def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)


# returns an ID for the order submitted
def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }
    r = requests.post(ORDER_URL, json=data, headers=HEADERS)
    return json.loads(r.content)


def get_orders():
    r = requests.get(ORDER_URL, headers=HEADERS)
    return json.loads(r.content)
