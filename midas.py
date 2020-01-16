from logger import logger


class Midas:
    """
    A midas object. What is it? I dunno. Ayla, fill this out
    """

    def __init__(self):
        # This gets run whenever a new Midas object is created
        logger.debug("Initialized a Midas object, {}".format(repr(self)))
        self.raw_data = None

    def train(self, file):
        """
        Train the model. Right now this just parses data from a CSV into a RawData object and prints it
        :param file:
        :return:
        """
        return True

    def start(self):
        """
        Start midas. Ayla, this is your entry point.
        :return:
        """
        logger.debug("stonks")
        logger.info("stocks")
        logger.warning("Stocks")
        logger.error("STOCKS")
        logger.critical("STOCKS!!!!!")
