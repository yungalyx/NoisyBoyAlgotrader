import requests, json
import alpaca_trade_api as tradeapi
from alpaca_trade_api import StreamConn
from src.setup import ENDPOINT_URL, SECRET_KEY, API_KEY

ACCOUNT_URL = '{}/v2/account'.format(ENDPOINT_URL)
ORDER_URL = '{}/v2/orders'.format(ENDPOINT_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}

class PaperTradingBot:

    def __init__(self):
        self.alpaca = tradeapi.REST(API_KEY, SECRET_KEY, ENDPOINT_URL, api_version='v2')

    def run(self):
        # on each minute
        async def on_minute(conn, channel, bar):
            if bar.close >= bar.open and bar.open - bar.low > 0.1:
                print("Buying on Doji Candle!")
                self.alpaca.submit_order("MSFT", 1, 'buy', 'market', 'day')
        self.conn = StreamConn('Polygon Key', 'Polygon Key', 'wss://alpaca.socket.polygon.io/stocks')
        on_minute = self.conn('r' )

            # TODO: create a take profit function at 1% more



'''
bd = PaperTradingBot()
bd.run
'''

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


create_order()
