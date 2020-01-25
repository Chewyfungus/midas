#!/usr/bin/env python
# coding: utf-8

# In[ ]:


period = 10
data_tis, meta_data_ti = ti.get_rsi(symbol='AAPL', interval='1min', time_period=period, series_type='close')
rsi = data_tis
rsi = rsi.reset_index()

aapl_data, meta_data = ts.get_intraday(symbol='AAPL', outputsize='full', interval='1min')
meta_data_aapl = {'source': "Alpha Vantage"}
aapl_data = aapl_data.rename(columns={'4. close': 'price'})
aapl_data = aapl_data.rename(columns={'1. open': 'open'})
aapl_data['index'] = aapl_data.index
aapl_data = aapl_data.reset_index()

rsic = rsi.set_index('date').join(aapl_data.set_index('date'))

# Merge RSI and Price data

rsic = rsic.reset_index()

rsic.to_csv("C:\\Users\\shadeh\\Documents\\4vs9.csv")


# In[ ]:


rsic = pd.read_csv("C:\\Users\\shadeh\\Documents\\4vs9.csv")

rsic['pchange'] = rsic['price'] - rsic['open']

rsic['strat'] = 0

market = (rsic['price'].iloc[0] - rsic['price'].iloc[-1])

for i in range(10, 1900):
    
    if rsic.loc[i, 'RSI'] > 70:
    
        #Sell when RSI dips back below 70
        
        rsic.loc[i, 'strat'] = 1  

        #Buy when RSI dips above 70

    elif rsic.loc[i, 'RSI'] < 31:
      
        rsic.loc[i, 'strat'] = -1

    else:
        rsic.loc[i, 'strat'] = 0

# Organize past trades

rsic['stratlag'] = rsic['strat'].shift(-1)

rsic = rsic[rsic.stratlag != 0]

#Corresponding price to each trade

rsic['warret'] = rsic['price'] * rsic['stratlag']

rsic = rsic.loc[rsic['stratlag'].shift(1) != rsic['stratlag']]

rsic = rsic.fillna(0)

rsic.to_csv("C:\\Users\\shadeh\\Documents\\backtest.csv")

dough = sum(rsic['warret'])

flop = sum(rsic['stratlag'])

if flop == -1:
    asset = dough + rsic['price'].iloc[0]
elif flop == 0:
    asset = dough
else:
    asset = dough - rsic['price'].iloc[0]

                                        
alpha = asset - market

print(alpha, asset, market, flop)

