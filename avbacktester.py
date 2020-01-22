#!/usr/bin/env python
# coding: utf-8

# In[3]:


get_ipython().system('pip install git+https://github.com/manahl/arctic.git')
from datetime import datetime as dt
import pandas as pd
import numpy as np
get_ipython().system('pip install alpaca-trade-api')
import alpaca_trade_api as tradeapi
from arctic import Arctic
get_ipython().system('pip install alphavantage')
get_ipython().system('pip install alpha_vantage')
from alpha_vantage import timeseries
import os 
get_ipython().system('pip install git+https://github.com/RomelTorres/alpha_vantage.git@develop')
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import time
get_ipython().system('pip install schedule')
import schedule


# In[4]:


store = Arctic('localhost')
store.initialize_library('HISTORICAL_DATA')
library = store['HISTORICAL_DATA']
key = os.path.expandvars("0N2O6RYAETJXM7QR")
ts = TimeSeries(key, output_format='pandas')
aapl_data, meta_data = ts.get_intraday(symbol='AMZN', outputsize='full', interval='1min')
meta_data_aapl = {'source': "Alpha Vantage"}
library.write('AMZN', aapl_data, metadata=meta_data_aapl)
item = library.read('AMZN')
aapl = item.data
rawdata = item.metadata
aapl_data, meta_aapl_data = ts.get_intraday('AMZN')
API_KEY = 'Alpaca-Api-Key-Here'
SECRET_KEY = 'Alpaca-Secret-Key-Here'
api = tradeapi.REST(API_KEY,SECRET_KEY,'https://paper-api.alpaca.markets', api_version='v2')
account = api.get_account()
ti = TechIndicators(key, output_format='pandas')
HEADER = {API_KEY, SECRET_KEY}
positions = "/v2/positions/".format("https://paper-api.alpaca.markets")


# In[37]:


#Ema cross signal download from AV

period = 4
data_tis, meta_data_ti = ti.get_ema(symbol='AMZN', interval='1min', time_period=period, series_type='close')
emas = data_tis.iloc[::-1]
emas = emas.rename(columns={'EMA': 'emas'})
emas = emas.reset_index()
period = 7
data_til, meta_data_ti = ti.get_ema(symbol='AMZN', interval='1min', time_period=period, series_type='close')
emal = data_til.iloc[::-1]
emal = emal.rename(columns={'EMA': 'emal'})
emal = emal.reset_index()
emacross = emal.set_index('date').join(emas.set_index('date'))
emac = emacross['emas'] - emacross['emal']
emac

aapl_data, meta_data = ts.get_intraday(symbol='AMZN', outputsize='full', interval='1min')
meta_data_aapl = {'source': "Alpha Vantage"}
aapl_data = aapl_data.rename(columns={'4. close': 'price'})
aapl_data = aapl_data.rename(columns={'1. open': 'open'})
aapl_data['index'] = aapl_data.index
aapl_data = aapl_data.reset_index()
aapl_data

emac = emac.reset_index()
emaspread = emac.set_index('date').join(aapl_data.set_index('date'))
emaspread = emaspread.reset_index()

emaspread.to_csv("C:\\Users\\shadeh\\Documents\\4vs9.csv")


# In[5]:


#Reverse Ops strategy

cross1 = pd.read_csv("C:\\Users\\shadeh\\Documents\\4vs9.csv")

cross = cross1.rename(columns = {"0" : "emacross"})

cross['change'] = cross['open'] - cross['price']

#Buy when EMA cross is +, sell when -

cross['buy'] = (cross.emacross >= 0).astype('int')
cross['buy1'] = cross['buy'].shift(-1)

#Sale occurs during first crossover period

cross['sale'] = cross['buy'] - cross['buy1']

cross['strat'] = 0

#For loop through time series testing strategy

for i in range(1, 1800):
    
    #Two periods without crossovers required 
    
    if cross.loc[i+1, 'sale'] == 0 and cross.loc[i+2, 'sale'] == 0:
    
        #Buy

        # + - - -

        if cross.loc[i, 'emacross'] > 0 and cross.loc[i+1, 'emacross'] < 0 and cross.loc[i+2, 'emacross'] < 0:
            cross.loc[i, 'strat'] = 1  

        #Sell

        # - + + +

        elif cross.loc[i, 'emacross'] < 0 and cross.loc[i+1, 'emacross'] > 0 and cross.loc[i+2, 'emacross'] > 0:
            cross.loc[i, 'strat'] = -1

    #Reverse the above strategy when crossover has occurred within two periods prior
            
    elif cross.loc[i+1, 'sale'] != 0 or cross.loc[i+2, 'sale'] != 0:
        
        #BUY
        
        # - + -

        if cross.loc[i, 'emacross'] < 0 and cross.loc[i+1, 'emacross'] > 0 and cross.loc[i+2, 'emacross'] < 0 and cross.loc[i, 'sale'] > 0:
            cross.loc[i, 'strat'] = 1

            
        #SELL
       
        # + - +

        elif cross.loc[i, 'emacross'] > 0 and cross.loc[i+1, 'emacross'] < 0 and cross.loc[i+2, 'emacross'] > 0 and cross.loc[i+1, 'sale'] < 0:
            cross.loc[i, 'strat'] = -1


      

    else:
            cross.loc[i, 'strat'] = 0
        
cross.to_csv("C:\\Users\\shadeh\\Documents\\backtest.csv")

cross = cross[cross.strat != 0]

cross = cross.loc[cross['strat'].shift(-1) != cross['strat']]

cross['warret'] = cross['price'] * cross['strat']
        


# In[6]:


#Results of strategy (Alpha) vs. market returns

dough = sum(cross['warret'])

flop = sum(cross['strat'])

market = (cross['price'].iloc[0] - cross['price'].iloc[-1])

if flop == -1:
    asset = dough + cross['price'].iloc[0]
elif flop == 0:
    asset = dough
else:
    asset = dough - cross['price'].iloc[0]
    
alpha = asset - market

print(alpha, asset, market, flop)


# In[7]:


#Aroon download

period = 8
data_tis, meta_data_ti = ti.get_aroon(symbol='AAPL', interval='1min', time_period=period, series_type='close')
aroon = data_tis

aapl_data, meta_data = ts.get_intraday(symbol='AAPL', outputsize='full', interval='1min')
meta_data_aapl = {'source': "Alpha Vantage"}
aapl_data = aapl_data.rename(columns={'4. close': 'price'})
aapl_data = aapl_data.rename(columns={'1. open': 'open'})
aapl_data['index'] = aapl_data.index
aapl_data = aapl_data.reset_index()


aroon = aroon.reset_index()
aroonc = aroon.set_index('date').join(aapl_data.set_index('date'))
aroonc = aroonc.reset_index()
aroonc.to_csv("C:\\Users\\shadeh\\Documents\\4vs9.csv")


# In[8]:


#Aroon oscillator results, same as EMA results


aroonc = pd.read_csv("C:\\Users\\shadeh\\Documents\\4vs9.csv")

aroonc['strat'] = 0

aroonc['spread'] = aroonc['Aroon Up'] - aroonc['Aroon Down']

aroonc['buy'] = (aroonc.spread <= 0).astype('int')
aroonc['buy1'] = aroonc['buy'].shift(-1)

aroonc['sale'] = aroonc['buy'] - aroonc['buy1']

for i in range(1, 1900):
    
    if aroonc.loc[i+1, 'sale'] == 0 and aroonc.loc[i+2, 'sale'] == 0:
    
        #Buy

        # + - - -

        if aroonc.loc[i, 'spread'] > 0:
            aroonc.loc[i, 'strat'] = -1  

        #Sell

        # - + + +

        elif aroonc.loc[i, 'spread'] < 0:
            aroonc.loc[i, 'strat'] = 1

    else:
            aroonc.loc[i, 'strat'] = 0
        
aroonc.to_csv("C:\\Users\\shadeh\\Documents\\backtest.csv")        

aroonc = aroonc[aroonc.strat != 0]

aroonc = aroonc.loc[aroonc['strat'].shift(-1) != aroonc['strat']]

aroonc['warret'] = aroonc['price'] * aroonc['strat']

dough = sum(aroonc['warret'])

flop = sum(aroonc['strat'])


market = (aroonc['price'].iloc[0] - aroonc['price'].iloc[-1])

if flop == -1:
    asset = dough + aroonc['price'].iloc[0]
elif flop == 0:
    asset = dough
else:
    asset = dough - aroonc['price'].iloc[0]
    

                                        
alpha = asset - market

print(alpha, asset, market, flop)

