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
        train_data = pd.DataFrame(pd.read_csv("data/gold_futures_train.csv",))
        test_data = pd.DataFrame(pd.read_csv("data/gold_futures_test.csv"))

        cols0 = ["Price0", "Open0", "High0", "Low0"]
        cols1 = ["Price1", "Open1", "High1", "Low1"]

        train_data[cols0] = train_data[cols0].replace({'\$': '', ',': ''}, regex=True)
        test_data[cols1] = test_data[cols1].replace({'\$': '', ',': ''}, regex=True)

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

        logger.info(train_data.head())

        logger.info(train_data.min())
        logger.info(test_data.max())
        # Max: 1613.3; Min: 255
        xmax = 1613.3
        xmin = 255.0

        scaler = preprocessing.MinMaxScaler()

        m_data = pd.concat([train_data, test_data], axis=1)
        m_data.head()
        m_data[["Price0", "Open0", "Price1", "Open1"]] = scaler.fit_transform(m_data[["Price0", "Open0", "Price1", "Open1"]])
        # m_data["Price"] = train_data.apply(lambda x: self.p_scaled(x) if x.name == "Price" else x)

        logger.info(m_data.head())
    """    
    def p_std(self, x):
        return ((x - 255.0) / (1613.3 - 255.0))

    def p_scaled(self, x):
        scale = (1 / (1613.3 - 255.0)) - 255.0
        return (x * scale)
    """