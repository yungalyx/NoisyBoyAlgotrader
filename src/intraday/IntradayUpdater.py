import json, threading
import websocket
import dateutil.parser
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from src.setup import TIINGO_KEY

socket = 'wss://api.tiingo.com/iex'

current_tick = None  # tracking current tick
previous_tick = None

minute_candlesticks = pd.DataFrame(columns=['minute', 'open', 'high', 'low', 'close'])
minutes_processed = {}


def on_open(ws):
    print('=== Opened Connection ===')
    auth_data = {
        'eventName': 'subscribe',
        'authorization': TIINGO_KEY,
        'eventData': {
            'thresholdLevel': 5,
            'tickers': ['spy']
        }
    }
    ws.send(json.dumps(auth_data))


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


def grabdata():
    socket = 'wss://api.tiingo.com/iex'
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
    ws.run_forever()


thread = threading.Thread(target=grabdata)
thread.start()

app = dash.Dash()

fig = go.Figure(data=go.Ohlc(x=minute_candlesticks['minute'],
                             open=minute_candlesticks['open'],
                             high=minute_candlesticks['high'],
                             low=minute_candlesticks['low'],
                             close=minute_candlesticks['close']))

app.layout = html.Div([
    dcc.Graph(id='live-graph', figure=fig, animate=True),  # need id to update objects in js
    dcc.Interval(
        id='graph-update',
        interval=2*1000,
        n_intervals=0
    )
])


@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'interval')])
def update_graph():
    figure = {
        'data': [fig],
        'layout': go.Layout(xaxis=range(0, len(minute_candlesticks)))  # might need to update yaxis as well
    }
    return figure


app.run_server(debug=False)
