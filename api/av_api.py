from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from logger import logger
from stock import Stock
import datetime


def _get_api_key():
    try:
        with open("api_keys/alpha-vantage.api", "r") as f:
            api_key = f.read().rstrip()
        return api_key
    except FileNotFoundError:
        logger.error("No API key found for AlphaVantage. "
                     "Please get an API key and save it to api_keys/alpha-vantage.api")
        return None


def av_get_all_intraday(symbol, interval='1min'):
    """
    Get all the intraday data for a given stock symbol
    :param symbol: The stock symbol
    :param interval: The interval between data points
    :return: A list of Stock objects, ordered by time
    """
    logger.debug("AV API: Getting intraday for stock {} with interval {}".format(symbol.upper(), interval))
    data = TimeSeries(key=_get_api_key()).get_intraday(symbol=symbol.upper(), interval=interval)[0]
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


def av_get_all_sma(symbol, interval='daily', time_period=20, series_type='close'):
    """
    Get all the SMA data of a given stock
    :param symbol: str: The stock symbol
    :param interval: str: The interval between two consecutive data points.
            Function accepts 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly
    :param time_period: int The number of data points used to calculate the moving average
    :param series_type: str: The price type. Function accepts close, open, high, low
    :return: A list of (datetime, float) tuples in this format:
                [(date, sma), (date, sma), (date, sma) ... ]
                Items are ordered by date.
    """
    logger.debug("AV API: Getting AlphaVantage SMA for stock {}".format(symbol.upper()))
    data = TechIndicators(key=_get_api_key()).get_sma(symbol,
                                                      interval=interval,
                                                      time_period=time_period,
                                                      series_type=series_type)[0]
    ret = []
    for timestamp in data.keys():
        # Check to see if AV returned hours and minutes as well
        if len(timestamp) > 10:
            daytime = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
        else:
            daytime = datetime.datetime.strptime(timestamp, "%Y-%m-%d")
        sma = float(data[timestamp]["SMA"])
        ret.append((daytime, sma))
    ret.sort(key=lambda r: r[0])
    return ret
