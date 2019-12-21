import datetime
import logging

LOG_DIR = "logs"
LOG_FORMAT = "%(asctime)s [%(levelname)s]: %(message)s"

class Log:
    """
    This class is a generic logger. It logs to console and file.
    """

    def __init__(self, name,  level=logging.INFO, log_dir=LOG_DIR):
        # Set the logging verbosity
        self.logger_ = logging.getLogger(name)
        self.logger_.setLevel(level)

        # Set up the file handler so it logs to a file
        file_handler = logging.FileHandler(log_dir + "/midas_" + str(datetime.datetime.now().strftime("%y-%m-%d-%H:%M:%S")) + ".log")
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

        # Set up a stream handler so it logs to console
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))

        # Add the handlers to the logger
        self.logger_.addHandler(file_handler)
        self.logger_.addHandler(stream_handler)

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
