#!/usr/bin/env python
# encoding: utf-8
"""
Author: Yuan-Ping Chen
Data: 2016/11/05
"""


import numpy as np
np.random.seed(1337)
from keras.datasets import mnist
from keras.datasets import cifar10
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation, Convolution2D, MaxPooling2D, Flatten
from keras.optimizers import Adam

(X_train, y_train), (X_test, y_test) = mnist.load_data()
print 'Dimension after loading'
print ' X_train.shape: ', X_train.shape
print ' y_train.shape: ', y_train.shape
# data pre-processing 
X_train = X_train.reshape(-1, 1, 28, 28)
X_test = X_test.reshape(-1, 1, 28, 28)
y_train = np_utils.to_categorical(y_train, nb_classes=10)
y_test = np_utils.to_categorical(y_test, nb_classes=10)
print 'Dimension after reshaping'
print ' X_train.shape: ', X_train.shape
print ' y_train.shape: ', y_train.shape
# build model
model = Sequential()

# Conv layer 1 output shape (32, 28, 28)
model.add(Convolution2D(
    nb_filter=32,
    nb_row=5,
    nb_col=5,
    border_mode='same',     # Padding method
    dim_ordering='th',      # if use tensorflow, to set the input dimension order to theano ("th") style, but you can change it.
    input_shape=(1, 28, 28)    
))

model.add(Activation('relu'))

# Pooling layer 1 (max pooling) output shape (32, 14, 14)
model.add(MaxPooling2D(
    pool_size=(2, 2),
    strides=(2, 2),
    border_mode='same'))

# Conv layer 2 output shape (64, 14, 14)
model.add(Convolution2D(64, 5, 5, border_mode='same'))
model.add(Activation('relu'))

# Pooling layer 2 (max pooling) output shape (64, 7, 7)
model.add(MaxPooling2D(pool_size=(2, 3), border_mode='same'))

# Fully connected layer 1 input shape (64 * 7 * 7) = (3136), output shape (1024)
model.add(Flatten())
model.add(Dense(1024))
model.add(Activation('relu'))

# Fully connected layer 2 to shape (10) for 10 classes
model.add(Dense(10))
model.add(Activation('softmax'))

# Another way to define your optimizer
adam = Adam(lr=1e-4)

# We add metrics to get more results you want to see
model.compile(optimizer=adam,
              loss='categorical_crossentropy',
              metrics=['accuracy'])

print('Training ------------')
# Another way to train the model
print 'Dimension before training'
print ' X_train.shape: ', X_train.shape
print ' y_train.shape: ', y_train.shape
model.fit(X_train, y_train, nb_epoch=1, batch_size=32)

print('\nTesting ------------')
# Evaluate the model with the metrics we defined earlier
loss, accuracy = model.evaluate(X_test, y_test)

print('\ntest loss: ', loss)
print('\ntest accuracy: ', accuracy)


