import keras
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras.backend import set_session
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import Conv2D, Dense, Flatten, MaxPool2D
from keras.models import Sequential, load_model
from keras.optimizers import adam_v2
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator


class Net:
    def net_model(self):
        pass

    def train(self):
        pass

    def test(self):
        pass

    def delete_model(self):
        pass
