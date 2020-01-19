import csv
import tensorflow as tf
import numpy as np
from midas import logger
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class Gold:
    def __init__(self):
        logger.debug("Initialized a Gold object, {}".format(repr(self)))

    def test(self):
        train_data = pd.DataFrame(pd.read_csv("data/gold_futures_train.csv",))
        test_data = pd.DataFrame(pd.read_csv("data/gold_futures_test.csv"))

        cols = ["Price", "Open", "High", "Low"]

        train_data[cols] = train_data[cols].replace({'\$': '', ',': ''}, regex=True)
        test_data[cols] = test_data[cols].replace({'\$': '', ',': ''}, regex=True)

        train_data["Date"] = pd.to_datetime(train_data["Date"])
        train_data["Price"] = pd.to_numeric(train_data["Price"])
        train_data["Open"] = pd.to_numeric(train_data["Open"])
        train_data["High"] = pd.to_numeric(train_data["High"])
        train_data["Low"] = pd.to_numeric(train_data["Low"])

        test_data["Date"] = pd.to_datetime(train_data["Date"])
        test_data["Price"] = pd.to_numeric(test_data["Price"])
        test_data["Open"] = pd.to_numeric(test_data["Open"])
        test_data["High"] = pd.to_numeric(test_data["High"])
        train_data["Low"] = pd.to_numeric(train_data["Low"])

        logger.info(train_data.head())

        logger.info(train_data.min())
        logger.info(test_data.max())
        # Max: 1613.3; Min: 255
        xmax = 1613.3
        xmin = 255.0

        m_train_data = train_data
        m_train_data["Price", "Open"] = train_data.apply(lambda x: self.p_scaled(x) if x.name in ["Price","Open"] else x)
        logger.info(train_data.head())
        # test_data["Price"] = pd.apply(self.p_scaled)

        # modDfObj = dfObj.apply(lambda x: np.square(x) if x.name in ['x', 'y'] else x)


        # X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
        # X_scaled = X_std * (max - min) + min

    def p_std(self, x):
        return ((x - 255.0) / (1613.3 - 255.0))

    def p_scaled(self, x):
        scale = (1 / (1613.3 - 255.0)) - 255.0
        return x