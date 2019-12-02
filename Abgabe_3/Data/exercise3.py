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
import math

"""
Excersise 3:
Implement the Pearson correlation coefficient.
Do NOT use any given function for standard-deviation or mean-value but implement them by yourself.

X, Y are given as lists.

Blockwise application is done outside so please use the whole vectors at once.
"""
def correlation(X, Y):
	mittelwert_x = 0.0
	mittelwert_y = 0.0

	for i in range(0,len(X)):
		mittelwert_x+=X[i] 
		mittelwert_y+=Y[i] 
	mittelwert_x/=len(X)
	mittelwert_y/=len(Y)

	oben = 0.0
	unten_1 = 0.0
	unten_2 = 0.0
	for i in range(0,len(X)):
		oben += (X[i]-mittelwert_x)*(Y[i]-mittelwert_y)
		unten_1 += (X[i]-mittelwert_x)**2.0
		unten_2 += (Y[i]-mittelwert_y)**2.0
	z = math.sqrt(unten_1*unten_2)
	if z != 0:
		return (oben/z)
	else:
		return (0)


"""
Example mean-quantizer.
"""
def quant0(A, B, E, args):  # A, B, E are lists. Args is not used here but might be necessary when it comes to Q1 and Q2.
    Q = lambda x, t: 1 if x > t else 0  # Q maps to 1 if x>t. Otherwise Q maps to 0.
    bA = map(Q, A, [numpy.mean(A) for i in range(len(A))])  # bA[i]=Q(A[i], mean(A))
    bB = map(Q, B, [numpy.mean(B) for i in range(len(B))])
    bE = map(Q, E, [numpy.mean(E) for i in range(len(E))])
    return bA, bB, bE

