import csv
import datetime
from stock import Stock


def yhf_get_data(file, symbol):
    with open(file, "r") as f:
        data = []
        for row in csv.reader(f):
            s = Stock()
            day = None
            try:
                # We need to manually parse the date
                day = datetime.datetime.strptime(row[0], "%Y-%m-%d")
            except ValueError:
                pass
            if s.populate(symbol.upper(), day, row[1], row[2], row[3], row[4], row[5], row[6]):
                data.append(s)
    return data
