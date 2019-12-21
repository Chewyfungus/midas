from logger import Log
import logging


class Midas:
    """
    A midas object. What is it? I dunno. Ayla, fill this out
    """

    def __init__(self):
        # This gets run whenever a new Midas object is created
        self.main_logger = Log("MainLog", level=logging.DEBUG)
        self.main_logger.debug("Initialized MainLog")
        self.main_logger.debug("Initialized a Midas object, {}".format(repr(self)))

    def start(self):
        """
        Start midas. Ayla, this is your entry point.
        :return:
        """
        self.main_logger.debug("stonks")
        self.main_logger.info("stocks")
        self.main_logger.warning("Stocks")
        self.main_logger.error("STOCKS")
        self.main_logger.critical("STOCKS!!!!!")
