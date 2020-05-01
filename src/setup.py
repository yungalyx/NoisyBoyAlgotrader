import bs4 as bs
import pickle
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web

SECRET_KEY = 'MT6ZPUdqChaXPF/fdz/P7zCUihYDNlnvSbhF8ZeZ'
API_KEY = 'PKAEF0MF359GKY0XS5SK'
ENDPOINT_URL = 'https://paper-api.alpaca.markets'

TIINGO_KEY = '3b766e3ad439feb379b9b2cdd0e677761ae72842'
# authenticate message for TIINGO


response = {'service': 'iex',
            'messageType': 'A',
            'data': ['T', '2020-04-29T10:35:15.491012812-04:00', 1588170915491012812, 'spy',
                     None, None, None, None, None, 292.27, 100, None, 0, 0, 0, 0]}
