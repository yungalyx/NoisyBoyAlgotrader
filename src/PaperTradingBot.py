import requests, json, websocket
from websocket import create_connection
import alpaca_trade_api as tradeapi
import dateutil.parser
from src.setup import ENDPOINT_URL, SECRET_KEY, API_KEY, TIINGO_KEY

ACCOUNT_URL = '{}/v2/account'.format(ENDPOINT_URL)
ORDER_URL = '{}/v2/orders'.format(ENDPOINT_URL)
DATA_URL = 'https://data.alpaca.markets/v1'
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
TICKER = ['AAPL', 'RACE', 'TSLA']

# for processing intraday data stream
minutes_processed = {}  # dictionary
minute_candlesticks = []  # a list of minute candlesticks
current_tick = None  # tracking current tick
previous_tick = None


class PaperTradingBot:

    # this function not used until bot is deployed
    def __init__(self):
        self.alpaca = tradeapi.REST(API_KEY, SECRET_KEY, ENDPOINT_URL, api_version='v2')
        self.alpacadata = tradeapi.REST(API_KEY, SECRET_KEY, DATA_URL)

    def run(self):
        barset = self.alpaca.get_barset('AAPL', 'day', limit=3)

    def on_open(ws):
        print('=== Opened Connection ===')
        # authenticate
        auth_data = {
            'eventName': 'subscribe',
            'authorization': TIINGO_KEY,
            'eventData': {
                'thresholdLevel': 5,
                'tickers': ['uso', 'spy']
            }
        }
        ws.send(json.dumps(auth_data))

    # do not listen to the IDE... this method is NOT static
    def on_message(ws, message):
        global current_tick, previous_tick
        previous_tick = current_tick
        current_tick = json.loads(message)

        if current_tick['messageType'] == 'A':

            print('==+ RECEIVED TICK +==')
            tick_price = current_tick['data'][9]
            print('{} @ {}'.format(current_tick['data'][1], tick_price))
            tick_datetime_obj = dateutil.parser.parse(current_tick['data'][1])
            tick_dt = tick_datetime_obj.strftime('%m/%d/%Y %H:%M')  # minute is smallest factor of change

            # checking for new minute
            if tick_dt not in minutes_processed:
                print('Starting new candlestick')
                minutes_processed[tick_dt] = True
                print(minutes_processed)

            if len(minute_candlesticks) > 0:
                minute_candlesticks[-1]['close'] = previous_tick['price']

            minute_candlesticks.append({
                'minute': tick_dt,
                'open': tick_price,
                'high': tick_price,
                'low': tick_price,
            })

            if len(minute_candlesticks) > 0:
                current_candlestick = minute_candlesticks[-1]
                if tick_price > current_candlestick['high']:
                    current_candlestick['high'] = tick_price
                if current_tick < current_candlestick['low']:
                    current_candlestick['low'] = tick_price

                print('===CANDLE-STICKS===')
                for candlesticks in minute_candlesticks:
                    print(candlesticks)

        else:
            print(current_tick)

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
