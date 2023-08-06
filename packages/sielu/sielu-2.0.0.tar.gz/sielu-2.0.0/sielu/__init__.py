from __future__ import division, print_function
import numpy as np
import tensorflow as tf
from keras.layers import LeakyReLU
from keras.utils.generic_utils import get_custom_objects

# Add the GELU function to Keras
def sielu(x):
    return 0.5 * x * (1 + tf.sigmoid(tf.sqrt(2 / np.pi) * (x + 0.044715 * tf.pow(x, 3))))
get_custom_objects().update({'sielu': sielu})
sielu = ['sielu']