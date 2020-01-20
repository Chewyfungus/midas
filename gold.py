import csv
import tensorflow as tf
import numpy as np
from sklearn import preprocessing
from midas import logger
import pandas as pd


class Gold:
    def __init__(self):
        logger.debug("Initialized a Gold object, {}".format(repr(self)))

    def test(self):
        train_data = pd.DataFrame(pd.read_csv("data/gold_futures_train.csv", ))
        test_data = pd.DataFrame(pd.read_csv("data/gold_futures_test.csv"))

        cols_train = ["PriceTrain", "OpenTrain", "HighTrain", "LowTrain"]
        cols_test = ["PriceTest", "OpenTest", "HighTest", "LowTest"]

        train_data[cols_train] = train_data[cols_train].replace({',': ''}, regex=True)
        test_data["PriceTest", "OpenTest", "HighTest",
                  "LowTest"] = test_data["PriceTest", "OpenTest", "HighTest",
                                         "LowTest"].replace({'\$': '', ',': ''}, regex=True)

        train_data["PriceTrain", "OpenTrain", "HighTrain",
                   "LowTrain"] = pd.to_numeric(train_data["PriceTrain", "OpenTrain", "HighTrain", "LowTrain"])
        test_data["PriceTest", "OpenTest", "HighTest",
                  "LowTest"] = pd.to_numeric(test_data["PriceTest", "OpenTest", "HighTest", "LowTest"])

        train_data["DateTrain"] = pd.to_datetime(train_data["DateTrain"])
        test_data["DateTest"] = pd.to_datetime(train_data["DateTest"])

        """
        train_data["Date0"] = pd.to_datetime(train_data["Date0"])
        train_data["Price0"] = pd.to_numeric(train_data["Price0"])
        train_data["Open0"] = pd.to_numeric(train_data["Open0"])
        train_data["High0"] = pd.to_numeric(train_data["High0"])
        train_data["Low0"] = pd.to_numeric(train_data["Low0"])

        test_data["Date1"] = pd.to_datetime(train_data["Date1"])
        test_data["Price1"] = pd.to_numeric(test_data["Price1"])
        test_data["Open1"] = pd.to_numeric(test_data["Open1"])
        test_data["High1"] = pd.to_numeric(test_data["High1"])
        test_data["Low1"] = pd.to_numeric(test_data["Low1"])
        """

        logger.info(train_data.min())
        logger.info(test_data.max())
        # Max: 1613.3; Min: 255
        xmax = 1613.3
        xmin = 255.0

        scaler = preprocessing.MinMaxScaler()

        m_data = pd.concat([train_data, test_data], axis=1)
        m_data.head()
        m_data[[cols_train_PO, cols_test_PO]] = scaler.fit_transform(m_data[[cols_train_PO, cols_test_PO]])
        # m_data["Price"] = train_data.apply(lambda x: self.p_scaled(x) if x.name == "Price" else x)

        logger.info(m_data.head())

    """    
    def p_std(self, x):
        return ((x - 255.0) / (1613.3 - 255.0))

    def p_scaled(self, x):
        scale = (1 / (1613.3 - 255.0)) - 255.0
        return (x * scale)
    """
