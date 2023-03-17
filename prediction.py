import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf 
import numpy as np
import skimage.measure
import matplotlib.pyplot as plt

model = tf.keras.models.load_model("keras.h5")

with open('class_names.txt') as f:
    class_names = [line.strip() for line in f.readlines()]

#print('Classes used in training:\n',class_names)

def predict(l):
    '''Handles converting input into usable format and making predictions.'''
    array = np.array(l)

    reduced_array = skimage.measure.block_reduce(array, (10, 10), np.mean)
    reduced_array = np.rot90(reduced_array, +3) # fixes array being rotated when converting from list -> np.array
    reduced_array = tf.expand_dims(reduced_array, axis=0)

    # Makes prediction and gets top 5
    predictions = model.predict(reduced_array)[0]
    top = (-pred).argsort()[:5]

    # Gets classification for guess
    guesses = [class_names[x] for x in ind]

    return gusses