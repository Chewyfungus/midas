from alpha_vantage.timeseries import TimeSeries
from logger import logger
import os
import datetime
import json
import schedule
import time


class AlphaVantageStock:
    def __init__(self, symbol):
        try:
            with open("api_keys/alpha-vantage.api", "r") as f:
                self.api_key = f.read().rstrip()
        except FileNotFoundError:
            logger.error("No API key found for AlphaVantageScraper at {}. "
                         "Please get an API key and save it to api_keys/alpha-vantage.api".format(self))
            return
        logger.debug("Using AlphaVantage API Key {} for {}".format(self.api_key, self))
        self.stock_symbol = symbol.upper()
        self.time_series = TimeSeries(key=self.api_key)

    def log_intraday(self, interval="1min"):
        """
        Log all the intraday trade data for the given stock
        :param interval: The default interval time, default 1 minute
        :return: nothing
        """
        dir = "data/alpha_vantage_intraday/{}".format(self.stock_symbol)
        if not os.path.exists(dir):
            os.makedirs(dir)
        data = self.time_series.get_intraday(symbol=self.stock_symbol, interval=interval)
        data = {"stock_data": data[0], "scrape_info": data[1]}
        with open(dir + "/" + datetime.datetime.now().strftime("%y-%m-%d.json"), "w+") as f:
            f.write(json.dumps(data))


class AlphaVantageScraper:

    def __init__(self, stock_limit=500):
        self.av_stock_objs = []
        with open("scrapers/alpha_vantage/stock_list.txt") as f:
            limit = 1
            for line in f:
                if limit > stock_limit:
                    logger.warning("Hit the max amount of stocks for the AlphaVantageScraper object at {}".format(self))
                    return
                self.av_stock_objs.append(AlphaVantageStock(line.rstrip().upper()))
                limit = limit + 1

    def init_schedule(self, calls_per_minute=5):
        """
        Schedule all the AlphaVantageStock objects to log intraday data when the markets close. Stagger them so we don't
        hit our API call limit.
        :param calls_per_minute: The calls per minute for the Alpha Vantage API. Free tier is 5 calls per minute, max
        500 per day.
        :return: nothing
        """
        sched_time = datetime.datetime.strptime("17:01:00", "%H:%M:%S")
        for stock in self.av_stock_objs:
            schedule.every().day.at(sched_time.strftime("%H:%M:%S")).do(stock.log_intraday)
            logger.debug("Scheduling logging for stock {} at {} times per minute starting at {}".format(stock.stock_symbol, calls_per_minute, sched_time.strftime("%H:%M:%S")))
            sched_time = sched_time + datetime.timedelta(seconds=(60/calls_per_minute) + 1)

    def run_scraper(self):
        """
        Run the scraper forever, continually collecting data every day when the markets close
        :return: never
        """
        while True:
            schedule.run_pending()
            time.sleep(1)
