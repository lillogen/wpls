#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

##############################################
##############################################
##   PhySec-Praktikum Framework 2019        ##
##   Authors: Jeremy Brauer                 ##
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
from subprocess import check_output

"""
Excersise Bit Error Rate:
Implement the Bit Error Rate computation.
Do NOT use any given function for but implement them by yourself.

X, Y are given as lists.

Blockwise application is done outside so please use the whole vectors at once.
"""


def ber(X, Y):
    return utils.not_yet_implemented("BER")


"""
Function call for entropy estimation.
Do not change this code
"""


def MI(A, B):
    if len(A) != len(B):
        raise ValueError("A and B must have the same length")
    with open("MI_temp.dat", "w+") as tmp:
        for (a, b) in zip(A, B):
            tmp.write("%f %f\n" % (a, b))
    return float(check_output(["./MIhigherdim", "MI_temp.dat", "2", "1", "1", "%d" % len(A), "8"]))


"""
Example mean-quantizer.
"""
def quant0(A, B, E, args):  # A, B, E are lists. Args is not used here but might be necessary when it comes to Q1 and Q2.
    Q = lambda x, t: 1 if x > t else 0  # Q maps to 1 if x>t. Otherwise Q maps to 0.
    bA = map(Q, A, [numpy.mean(A) for i in range(len(A))])  # bA[i]=Q(A[i], mean(A))
    bB = map(Q, B, [numpy.mean(B) for i in range(len(B))])
    bE = map(Q, E, [numpy.mean(E) for i in range(len(E))])
    return bA, bB, bE


"""
Implement the quantization scheme found in "Jana, Suman - 2009 - On the effectiveness of secret key extraction from wireless signal strength in real environments". 
You are provided with measurements for Node A, B and E.
Please return a binary list in bA, bB, bE as tuple.

Blockwise application is done outside so please use the whole datasets.
"""
def quant1(A, B, E, args):
    bA = []
    bB = []
    bE = []

    # Number of bits per symbol (parameter)
    number_of_bits = args.bits;
    # After you have finished, bA, bB and bE should be of same length and should be of the form [1, 0, 0, 1, 1, 1 ...]

    ### YOUR CODE GOES HERE ###

    return utils.not_yet_implemented("quant1")
    # return (bA, bB, bE) #After implementation, return binary vectors as tuple


def quant2(A, B, E, args):
    bA = []
    bB = []
    bE = []

    ## Better do not change the parameter validation
    alpha = args.alpha
    m = args.m
    if m % 2 == 0:  # check whether m is odd and change it if necessary
        m = m - 1
    """
    Wenn Wert größer q_plus = 1
    Wenn Wert kleiner q_minus = 0					
    q_plus >= Wert >= q_minius --> -1
    "-1" für Alice und Bob unbrauchbar
    """

    ### YOUR CODE GOES HERE ###

    return not_yet_implemented("quant2")

    # return bA, bB, bE  # After implementation, return binary vectors as tuple

