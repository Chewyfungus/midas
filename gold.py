import csv
import tensorflow as tf
import numpy as np
from midas import logger
import pandas as pd


class Gold:
    def __init__(self):
        logger.debug("Initialized a Gold object, {}".format(repr(self)))

    def test(self):
        train_data = pd.read_csv("data/gold_futures_train.csv")

        test_data = pd.read_csv("data/gold_futures_test.csv")

        logger.info(train_data.head())