# -*- coding: utf-8 -*-

###################################################################################
#    Function : loadmnistdata                                                     #
#    Purpose  : This is an independent function call to load the mnist image      #
#               datset that contains images of numbers from 0 to 9 primarily      #
#               used as a training and test dats sets for image processing        #
#               ML algorithms.                                                    #
#               This is built as an independent function to decouple the data     #
#               set loads and make the other functions independent of the dataset #
#                                                                                 #
###################################################################################

from tensorflow.keras.datasets import mnist

def loadmnistdata():
    (X_train, Y_train), (X_test, Y_test) = mnist.load_data()
    return X_train,Y_train,X_test,Y_test