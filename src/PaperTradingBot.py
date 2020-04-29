import requests, json, websocket
from websocket import create_connection
import alpaca_trade_api as tradeapi
from alpaca_trade_api import StreamConn
import pandas as pd
from src.setup import ENDPOINT_URL, SECRET_KEY, API_KEY, TIINGO_KEY

ACCOUNT_URL = '{}/v2/account'.format(ENDPOINT_URL)
ORDER_URL = '{}/v2/orders'.format(ENDPOINT_URL)
DATA_URL = 'https://data.alpaca.markets/v1'
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
TICKER = ['AAPL', 'RACE', 'TSLA']


class PaperTradingBot:

    # this function not used until bot is deployed
    def __init__(self):
        self.alpaca = tradeapi.REST(API_KEY, SECRET_KEY, ENDPOINT_URL, api_version='v2')
        self.alpacadata = tradeapi.REST(API_KEY, SECRET_KEY, DATA_URL)

    def run(self):
        barset = self.alpaca.get_barset('AAPL', 'day', limit=3)

    def on_open(ws):
        print('opened connection!')
        subscribe = {
            'eventName': 'subscribe',
            'authorization': '3b766e3ad439feb379b9b2cdd0e677761ae72842',
            'eventData': {
                'thresholdLevel': 5,
                'tickers': ['uso', 'spy']
            }
        }
        ws.send(json.dumps(subscribe))

    # do not listen to the IDE... this method is NOT static
    def on_message(ws, message):
        print('received message')
        print(json.loads(message))

    socket = 'wss://api.tiingo.com/iex'
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
    ws.run_forever()

    # data = pd.read_json(barset)
    # print(data)


'''
bd = PaperTradingBot()
bd.run()
'''


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
