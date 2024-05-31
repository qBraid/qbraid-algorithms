#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##########################################################################################
#    Function : pcareduction                                                             #
#    Purpose  : This is a function call to perform linear dimensonality reduction using  #
#               principal component analysis(PCA)                                        # 
#               The data is linearly transformed onto a new coordinate system such       #
#               that the directions (principal components) capturing the largest         #
#               variation in the data can be easily identified.                          #
#                                                                                        #
#              The principal components of a collection of points in a real coordinate   #
#              space are a sequence of p unit vectors where the i-th vector is the       #
#              direction of a line that best fits the data while being orthogonal to     #
#              the first vectors. Here, a best-fitting line is defined as one            #
#              that minimizes the average squared perpendicular distance from the        #
#              points to the line. These directions (i.e., principal components)         #
#              constitute an orthonormal basis in which different individual dimensions  #
#              of the data are linearly uncorrelated. Many studies use the first two     #
#              principal components in order to plot the data in two dimensions and      #
#              to visually identify clusters of closely related data points.             #
#                                                                                        #
##########################################################################################

import loadmnistdata as lmd
#import csv
#import json

#import numpy

#from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def pcareduction():

    X_train,Y_train,X_test,Y_test = lmd.loadmnistdata()

    dim_pca=10

    pca= PCA(n_components=dim_pca)

    model_pca=pca.fit_transform(X_train[:,:,1])

    num_examples=1000

    xs=model_pca[:,1:num_examples]

    #numpy.savetxt("/Users/anjanathimmaiah/soorajprograms/datafiles/pcaredoutput.csv", xs,delimiter =",")

    return xs