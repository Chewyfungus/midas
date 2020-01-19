import csv
import tensorflow as tf
import numpy as np
from midas import logger
import pandas as pd


class Gold:
    def __init__(self):
        logger.debug("Initialized a Gold object, {}".format(repr(self)))

    def test(self):
        train_data = pd.DataFrame(pd.read_csv("data/gold_futures_train.csv",))
        train_data["Date"] = pd.to_datetime(train_data["Date"])
        train_data["Price"] = pd.to_numeric()
        train_data["Open"] = pd.to_numeric()
        train_data["High"] = pd.to_numeric()
        train_data["Low"] = pd.to_numeric()

        test_data = pd.DataFrame(pd.read_csv("data/gold_futures_test.csv"))
        test_data["Date"] = pd.to_datetime(train_data["Date"])
        test_data["Price"] = pd.to_numeric()
        test_data["Open"] = pd.to_numeric()
        test_data["High"] = pd.to_numeric()
        train_data["Low"] = pd.to_numeric()

        logger.info(train_data.head())

        logger.info(train_data.min())

        logger.info(test_data.max())


