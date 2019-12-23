#!/usr/bin/python3
# This file is just a scratchpad! Only use it for testing stuff.
# Do not put any real code here!

from scrapers.alpha_vantage.av_scraper import AlphaVantageStock, AlphaVantageScraper
# m = Midas()
# m.start()
# m.train("data/AAPL.csv")
# avs = AlphaVantageStock("TSLA")
# avs.log_intraday('1min')
avs = AlphaVantageScraper()
avs.init_schedule()