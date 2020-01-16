import datetime
from logger import logger


class Stock:
    """
    This class holds all the info on a stock at a given time
    """
    def __init__(self):
        self.time = None
        self.open_price = None
        self.high_price = None
        self.low_price = None
        self.close_price = None
        self.adj_close_price = None
        self.volume = None
        self.symbol = None

    def populate(self, symbol, time, open_price, high_price, low_price, close_price, adj_close_price, volume):
        """
        Populate a stock object.
        :param symbol: string: The stock symbol. Required, cannot be none
        :param time: string or datetime: The time that the stock data is valid. Required, cannot be none
        :param open_price: float: The opening stock price
        :param high_price: float: The high stock price
        :param low_price: float: The low stock price
        :param close_price: float: The closing stock price
        :param adj_close_price: float: The adjusted close price
        :param volume: int: The volume of the stock
        :return:
        """
        try:
            self.symbol = symbol.upper()
            # Try to handle different cases for the input time
            # Handle passing in a datetime.datetime object
            if type(time) == datetime.datetime:
                self.time = time
            # Handle a string of the datetime in this format:
            # YYYY-MM-DD_HH:MM:SS
            elif type(time) == str:
                self.time = datetime.datetime.strptime(time, '%Y-%m-%d_%H:%M:%S')
            else:
                logger.warning("Unable to parse date {} to populate stock object at {}".format(time, self))
                return False
            if open_price:
                self.open_price = float(open_price)
            if high_price:
                self.high_price = float(high_price)
            if low_price:
                self.low_price = float(low_price)
            if close_price:
                self.close_price = float(close_price)
            if adj_close_price:
                self.adj_close_price = float(adj_close_price)
            if volume:
                self.volume = int(volume)
        except Exception as e:
            logger.warning("Unable to populate data for stock with the following data:"
                           "Symbol: {}, Time: {}, Open Price: {}, High Price: {}, Low Price: {}, Close Price: {}, "
                           "Adjusted Close Price: {}, Volume: {}. Got exception {}".format(symbol,
                                                                                           time,
                                                                                           open_price,
                                                                                           high_price,
                                                                                           low_price,
                                                                                           close_price,
                                                                                           adj_close_price,
                                                                                           volume,
                                                                                           repr(e)))
            return False
        return True

    def __repr__(self):
        return "Symbol: {}, DateTime: {}, Open: ${}, High: ${}, Low: ${}, " \
               "Close: ${}, Adjusted Close: ${}, Volume: {}\n".format(
                                                                        self.symbol,
                                                                        self.time,
                                                                        self.open_price,
                                                                        self.high_price,
                                                                        self.low_price,
                                                                        self.close_price,
                                                                        self.adj_close_price,
                                                                        self.volume
                                                                    )
