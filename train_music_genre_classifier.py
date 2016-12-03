#!/usr/bin/env python
# encoding: utf-8
"""
Author: Yuan-Ping Chen
Data: 2016/11/05
"""

import os
import numpy as np
np.random.seed(1337)
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation, Convolution2D, MaxPooling2D, Flatten
from keras.optimizers import Adam
# from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
import multiprocessing as mp


def build_model():
    # build model
    model = Sequential()

    # Conv layer 1 output shape (32, 128, 2584)
    model.add(Convolution2D(
        nb_filter=32,
        nb_row=3,
        nb_col=3,
        border_mode='same',     # Padding method
        dim_ordering='th',      # if use tensorflow, to set the input dimension order to theano ("th") style, but you can change it.
        input_shape=(1,128, 2584)    
    ))
    model.add(Activation('relu'))
    # Pooling layer 1 (max pooling) output shape (32, 64, 646)
    model.add(MaxPooling2D(
        pool_size=(2, 4),
        strides=(2, 4),
        border_mode='same'))


    # Conv layer 2 output shape (64, 64, 646)
    model.add(Convolution2D(64, 3, 3, border_mode='same'))
    model.add(Activation('relu'))
    # Pooling layer 2 (max pooling) output shape (64, 32, 161.5)
    model.add(MaxPooling2D(pool_size=(2, 4), border_mode='same'))


    # Conv layer 3 output shape (128, 32, 161.5)
    model.add(Convolution2D(128, 3, 3, border_mode='same'))
    model.add(Activation('relu'))
    # Pooling layer 3 (max pooling) output shape (128, 16, 80.75)
    model.add(MaxPooling2D(pool_size=(2, 4), border_mode='same'))

    # # Conv layer 4 output shape (128, 32, 161.5)
    # model.add(Convolution2D(192, 3, 3, border_mode='same'))
    # model.add(Activation('relu'))
    # # Pooling layer 4 (max pooling) output shape (128, 16, 80.75)
    # model.add(MaxPooling2D(pool_size=(3, 5), border_mode='same'))


    # Fully connected layer 1 input shape (128 * 16 * 80.75) = (165376), output shape (1024)
    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Activation('relu'))

    # Fully connected layer 2 to shape (10) for 10 classes
    model.add(Dense(10))
    model.add(Activation('softmax'))

    # Another way to define your optimizer
    adam = Adam(lr=1e-5)

    # We add metrics to get more results you want to see
    model.compile(optimizer=adam,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model

def train_and_evaludate(X_train, X_test, y_train, y_test, model):

   

    print('Training ------------')
    # Another way to train the model
    model.fit(X_train, y_train, nb_epoch=1, batch_size=32)

    print('\nTesting ------------')
    # Evaluate the model with the metrics we defined earlier
    loss, accuracy = model.evaluate(X_test, y_test)

    print('\ntest loss: ', loss)
    print('\ntest accuracy: ', accuracy)



def load_data(data_path, data_save_path):
    
    file_path_all = []
    for root, dirs, files in os.walk(data_path):
        # print root
        files = [f for f in files if not f[0] == '.']
        # print 'root:', root
        for f in files:
            file_path = os.path.join(root, f)
            file_path_all+=[file_path]

    mup = mp.Pool(processes=20)
    data = np.array(mup.map(np.load, file_path_all))
    mup.close()
    mup.join()
    np.save(data_save_path+os.sep+'data.npy', data)

    return data

def main():
    data_path='/Users/Frank/Documents/UCSC/TIM_209/project/feature'
    data_save_path='/Users/Frank/Documents/UCSC/TIM_209/project'
    label_path='/Users/Frank/Documents/UCSC/TIM_209/project/label.txt'
    
    try:
        X=np.load(data_save_path+os.sep+'data.npy')
    except IOError:
        X=load_data(data_path, data_save_path)

    y=np.loadtxt(label_path).astype(int)

    print 'Splitting data into training set and testing set...'
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=10, stratify=y)
    
    train_mean=np.mean(X_train, axis=0)
    train_std=np.std(X_train, axis=0)
    X_train=(X_train-train_mean)/train_std
    X_test=(X_test-train_mean)/train_std

    # data pre-processing 
    print 'Reshape data to fit CNN input...'
    X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1], X_train.shape[2])
    X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1], X_test.shape[2])
    y_train = np_utils.to_categorical(y_train, nb_classes=10)
    y_test = np_utils.to_categorical(y_test, nb_classes=10)
    print 'X_train.shape: ', X_train.shape
    print 'X_test.shape: ', X_test.shape

    model = build_model()
    train_and_evaludate(X_train, X_test, y_train, y_test, model)

if __name__ == '__main__':
    main()


