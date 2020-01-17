import csv
import tensorflow as tf
import numpy as np
from midas import logger


class Gold:
    def __init__(self):
        logger.debug("Initialized a Gold object, {}".format(repr(self)))

    def test(self):
        train_file_path = tf.keras.utils.get_file("data/gold_futures_train.csv")
        test_file_path = tf.keras.utils.get_file("gold_futures_test.csv")
        np.set_printoptions(precision=3, suppress=True)



