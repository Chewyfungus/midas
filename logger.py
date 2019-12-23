import datetime
import logging
import os

LOG_DIR = "logs"
LOG_FORMAT = "%(asctime)s [%(levelname)s]: %(message)s"
LOG_LEVEL = logging.DEBUG

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

file_handler = logging.FileHandler(LOG_DIR + "/midas_" + str(datetime.datetime.now().strftime("%y-%m-%d-%H:%M:%S")) + ".log")
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
file_handler.setLevel(LOG_LEVEL)

logger.addHandler(file_handler)
