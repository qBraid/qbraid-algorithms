#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##################################################################################
#    Function : OneHotEncodeData                                                  #
#    Purpose  : This is an independent function call to load the mnist image      #
#               datset that contains images of numbers from 0 to 9 primarily      #
#               used as a training and test dats sets for image processing        #
#               ML algorithms.                                                    #
#               This is built as an independent function to decouple the data     #
#               set loads and make the other functions independent of the dataset #
#                                                                                 #
###################################################################################

import pcalocaldetuning as pld
#import numpy

from sklearn.preprocessing import OneHotEncoder

def OneHotEncodeData():
    xs=pld.pcalocaldetuning()
    encoder = OneHotEncoder(sparse_output=False)



    onehotencodeddata=encoder.fit_transform(xs)

    #print("onehotencodeddata shape ",onehotencodeddata.shape)

    #print("Onehot encoded data")

    #print(onehotencodeddata[1:50,1:20])
    
    return onehotencodeddata


    #numpy.savetxt("/Users/anjanathimmaiah/soorajprograms/datafiles/onehotencoded.csv", onehotencodeddata,delimiter =",")
