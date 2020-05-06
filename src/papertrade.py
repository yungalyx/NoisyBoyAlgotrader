from src.setup import API_KEY, ENDPOINT_URL, SECRET_KEY
import requests, json


ACCOUNT_URL = '{}/v2/account'.format(ENDPOINT_URL)
ORDER_URL = '{}/v2/orders'.format(ENDPOINT_URL)
DATA_URL = 'https://data.alpaca.markets/v1'
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
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
