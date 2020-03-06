import bs4 as bs
import pickle
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web


def scrape_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers)
    return tickers



def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = scrape_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f.read())

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2019, 1, 1)
    end = dt.datetime.now()

    for ticker in tickers[:50]:
         if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
             df = web.DataReader(ticker, 'yahoo', start, end)
             df.to_csv('stock_dfs/{}.csv'.format(ticker))
         else:
             print("Already have {}".format(ticker))
