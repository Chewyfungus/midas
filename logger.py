import datetime
import logging

LOG_DIR = "logs"


class Log:
    """
    This class is the main logger for midas. We might add more loggers later
    """

    def __init__(self, name,  level=logging.INFO, log_dir=LOG_DIR):
        # Set the logging verbosity
        logging.basicConfig(level=level)
        self.logger_ = logging.getLogger(name)

        # Set the file path and name of the logs
        handler = logging.FileHandler(log_dir + "/" + str(datetime.datetime.now()).replace(" ", "") + "_midas.log")
        handler.setLevel(level)

        # Create a logging format
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
        handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger_.addHandler(handler)

    def debug(self, msg):
        """
        Log with debug verbosity
        :param msg: The message to log
        :return: nothing
        """
        self.logger_.debug(msg)

    def info(self, msg):
        """
        Log with info verbosity. Use this for most logging events
        :param msg: The message to log
        :return: nothing
        """
        self.logger_.info(msg)

    def warning(self, msg):
        """
        Log with warning verbosity. Use this for warnings and unexpected behavior
        :param msg: The message to log
        :return: nothing
        """
        self.logger_.warning(msg)

    def error(self, msg):
        """
        Log with error verbosity. Use this when something goes wrong but the program won't crash
        :param msg: The message to log
        :return: nothing
        """
        self.logger_.error(msg)

    def critical(self, msg):
        """
        Log with critical verbosity. Use this for uncrecoverable errors
        :param msg: The message to log
        :return: nothing
        """
        self.logger_.critical(msg)
