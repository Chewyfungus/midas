import csv
import datetime
from logger import logger


class RawData:
    """
    This class takes a CSV file from Yahoo finance, parses it, and exposes the info in a useful format
    Usage:
        All data is stored in RawData.data as a list of DayData objects.
        Ex: Get the high price for the nth day
        RawData.data[n].high
    """

    def __init__(self, file):
        with open(file, "r") as f:
            self.data = []
            for row in csv.reader(f):
                d = DayData()
                if d.populate(row[0], row[1], row[2], row[3], row[4], row[5], row[6]):
                    self.data.append(d)
                else:
                    logger.debug("Unable to add row to RawData object. File: {}. Data: {}, {}, {}, {}. {}, {}, {}".format(file, row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    def __repr__(self):
        ret = "\n"
        for d in self.data:
            ret = ret + repr(d) + "\n"
        return ret


class DayData:
    """
    This class holds all the info on a stock for a given day
    """
    def __init__(self):
        self.date = None
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.adj_close = None
        self.volume = None

    def populate(self, date, open_price, high_price, low_price, close_price, adj_close_price, volume):
        try:
            self.date = datetime.datetime.strptime(date, '%Y-%m-%d')
            self.open = float(open_price)
            self.high = float(high_price)
            self.low = float(low_price)
            self.close = float(close_price)
            self.adj_close = float(adj_close_price)
            self.volume = int(volume)
            return True
        except ValueError:
            return False

    def __repr__(self):
        return "DateTime: {}, Open: ${}, High: ${}, Low: ${}, Close: ${}, Adjusted Close: ${}, Volume: {}".format(
            self.date,
            self.open,
            self.high,
            self.low,
            self.close,
            self.adj_close,
            self.volume
        )
