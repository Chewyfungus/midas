import csv
import tensorflow as tf
import numpy as np
from midas import logger
import pandas as pd


class Gold:
    def __init__(self):
        logger.debug("Initialized a Gold object, {}".format(repr(self)))

    def test(self):
        train_data = pd.DataFrame(pd.read_csv("data/gold_futures_train.csv"))

        """
        , dtype = {
            ""
        }
        """

        test_data = pd.DataFrame(pd.read_csv("data/gold_futures_test.csv"))

        logger.info(train_data.head())

        p_tr_max = train_data['High'].max()
        p_tr_min = train_data['Low'].min()

        p_te_max = test_data['High'].max()
        p_te_min = test_data['Low'].min()

        logger.info(p_tr_max)
        logger.info(p_tr_min)
        logger.info(p_te_max)
        logger.info(p_te_min)
