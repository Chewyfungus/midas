from alpha_vantage.timeseries import TimeSeries
from logger import logger
from stock import Stock
import datetime


def av_get_intraday(symbol, interval='1min'):
    try:
        with open("api_keys/alpha-vantage.api", "r") as f:
            api_key = f.read().rstrip()
    except FileNotFoundError:
        logger.error("No API key found for AlphaVantage. "
                     "Please get an API key and save it to api_keys/alpha-vantage.api")
        return None
    logger.debug("Getting AlphaVantage intraday for stock {} with interval {}".format(symbol.upper(), interval))
    data = TimeSeries(key=api_key).get_intraday(symbol=symbol.upper(), interval=interval)[0]
    ret = []
    for time in data.keys():
        d = data.get(time)
        time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        stock = Stock()
        stock.populate(symbol=symbol,
                       time=time,
                       open_price=d.get("1. open"),
                       high_price=d.get("2. high"),
                       low_price=d.get("3. low"),
                       close_price=d.get("4. close"),
                       adj_close_price=None,
                       volume=d.get("5. volume"))
        ret.append(stock)
    ret.sort(key=lambda r: r.time)
    return ret
