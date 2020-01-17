import tensorflow as tf
from logger import logger
from gold import Gold

class Midas:
    """
    A midas object. What is it? I dunno. Ayla, fill this out
    """

    def __init__(self):
        # This gets run whenever a new Midas object is created
        logger.debug("Initialized a Midas object, {}".format(repr(self)))
        self.raw_data = None

    def train(self):
        """
        """
        x_train = 0
        y_train = 0

        x_test = 0
        y_test = 0
        return True

    def start(self):
        """
        Start midas. Ayla, this is your entry point.
        :return:
        """

        G = Gold()
        G.test()

        logger.debug("stonks")
        logger.info("stocks")
        logger.warning("Stocks")
        logger.error("STOCKS")
        logger.critical("STOCKS!!!!!")
