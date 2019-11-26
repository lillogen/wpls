#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

##############################################
##############################################
##   PhySec-Praktikum Framework 2019        ##
##   Authors: Jan Zimmer                    ##
##            Jeremy Brauer                 ##
##                                          ##
##   Students:   <fill in your names>       ##
##               <fill in Matrikel-Nr>      ##
##               <fill in your names>       ##
##   Student-ID: <fill in Matrikel-Nr>      ##
##                                          ##
##   DO ONLY CHANGE MARKED FUNCTION BODIES  ##
##                                          ##
##############################################
##############################################


import utils
import numpy

"""
Excersise 3:
Implement the Pearson correlation coefficient.
Do NOT use any given function for standard-deviation or mean-value but implement them by yourself.

X, Y are given as lists.

Blockwise application is done outside so please use the whole vectors at once.
"""
def correlation(X, Y):
    return utils.not_yet_implemented("Correlation")


"""
Example mean-quantizer.
"""
def quant0(A, B, E, args):  # A, B, E are lists. Args is not used here but might be necessary when it comes to Q1 and Q2.
    Q = lambda x, t: 1 if x > t else 0  # Q maps to 1 if x>t. Otherwise Q maps to 0.
    bA = map(Q, A, [numpy.mean(A) for i in range(len(A))])  # bA[i]=Q(A[i], mean(A))
    bB = map(Q, B, [numpy.mean(B) for i in range(len(B))])
    bE = map(Q, E, [numpy.mean(E) for i in range(len(E))])
    return bA, bB, bE

