#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###################################################################################
#    Function : pcalocaldetuning                                                  #
#    Purpose  : This function is used to scale the range of the principal         #
#               components to a feasible range of local detuning. Later, for each #
#               image, each of the 10 scaled principal components are encoded     #
#               into each single local detuning for 10 atoms.                     #
#                                                                                 #
###################################################################################

import pcareduction as custpca

def pcalocaldetuning():
    
    print("Calling pcareduction")
    xs =custpca.pcareduction()
    
    print("In pca local detuning")
    
    delta_max=6.0
    spectral=max(abs(xs.max()),abs(xs.min()))
    print("xs.max()")
    xs.max()
    print("xs.min()")
    xs.min()
    print("spectral ",spectral)
    
    xs=(xs/spectral)*delta_max
    print(xs)    
    
    return(xs)