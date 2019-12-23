from alpha_vantage.timeseries import TimeSeries
from logger import logger


def av_get_intraday(symbol, interval='1min'):
    try:
        with open("api_keys/alpha-vantage.api", "r") as f:
            api_key = f.read().rstrip()
    except FileNotFoundError:
        logger.error("No API key found for AlphaVantage. "
                     "Please get an API key and save it to api_keys/alpha-vantage.api")
        return None
    logger.debug("Getting AlphaVantage intraday for stock {} with interval {}".format(symbol.upper(), interval))
    return TimeSeries(key=api_key).get_intraday(symbol=symbol.upper(), interval=interval)
