#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install git+https://github.com/manahl/arctic.git')
from datetime import datetime as dt
import pandas as pd
import numpy as np
from arctic import Arctic
get_ipython().system('pip install alpaca-trade-api')
import alpaca_trade_api as tradeapi
get_ipython().system('pip install alpha_vantage')
from alpha_vantage import timeseries
import os 
get_ipython().system('pip install git+https://github.com/RomelTorres/alpha_vantage.git@develop')
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import time


# In[3]:


store = Arctic('localhost')
store.initialize_library('HISTORICAL_DATA')
library = store['HISTORICAL_DATA']
key = os.path.expandvars("0N2O6RYAETJXM7QR")
ts = TimeSeries(key, output_format='pandas')
aapl_data, meta_data = ts.get_intraday(symbol='AAPL', outputsize='full', interval='1min')
meta_data_aapl = {'source': "Alpha Vantage"}
library.write('AAPL', aapl_data, metadata=meta_data_aapl)
item = library.read('AAPL')
aapl = item.data
rawdata = item.metadata
aapl_data, meta_aapl_data = ts.get_intraday('AAPL')
API_KEY = 'api_key'
SECRET_KEY = 'secret_key'
api = tradeapi.REST(API_KEY, SECRET_KEY,'https://paper-api.alpaca.markets', api_version='v2')
account = api.get_account()
ti = TechIndicators(key, output_format='pandas')
HEADER = {API_KEY, SECRET_KEY}


# In[ ]:


while(True):

    EMA2 = ti.get_ema('AAPL', interval='1min')[0].tail(2)['EMA'][0]
    EMA3 = ti.get_ema('AAPL', interval='1min')[0].tail(3)['EMA'][0]
    lagspread = EMA2 - EMA3

    time.sleep(60)
    EMA2 = ti.get_ema('AAPL', interval='1min')[0].tail(2)['EMA'][0]
    EMA3 = ti.get_ema('AAPL', interval='1min')[0].tail(3)['EMA'][0]
    spread = EMA2 - EMA3
    if spread < 0 and lagspread > 0:
        api.submit_order('AAPL', 1, 'buy', 'market', 'gtc')
    elif spread > 0 and lagspread < 0:
        api.submit_order('AAPL', 1, 'sell', 'market', 'gtc')        
    elif spread > 0 and lagspread > 0:
        api.submit_order('AAPL', 1, 'buy', 'market', 'gtc')
    elif spread < 0 and lagspread  < 0:
        api.submit_order('AAPL', 1, 'sell', 'market', 'gtc')
        
print(lagspread, spread)

