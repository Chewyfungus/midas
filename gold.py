import csv
import tensorflow as tf
import numpy as np
from midas import logger


class Gold:
    def __init__(self):
        logger.debug("Initialized a Gold object, {}".format(repr(self)))

    def test(self):
        with open("data/gold_futures_train.csv", newline='') as csvfile:
            training_data = csv.reader(csvfile)
            for row in training_data:
                print(', '.join(row))

        test_file_path = tf.keras.utils.get_file("gold_futures_test.csv")
        np.set_printoptions(precision=3, suppress=True)

