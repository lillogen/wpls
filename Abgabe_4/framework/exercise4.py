#!/usr/bin/env python3
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


from utils import gray_code
import numpy
from subprocess import check_output
import math


"""
Excersise Bit Error Rate:
Implement the Bit Error Rate computation.
Do NOT use any given function for but implement them by yourself.

X, Y are given as lists.

Blockwise application is done outside so please use the whole vectors at once.
"""


def ber(X, Y):
    le = len(X)
    hw_arg = numpy.bitwise_xor(X,Y)
    z = numpy.count_nonzero( hw_arg ==1 )
    ber = float(z)/le
    if ber > 0.5:
        return 1 - ber + 1.0/le #Wenn X = inv(Y) ist die Biterrorrate = 1 bit und nicht 0, daher plus 1/le
    else: 
        return ber


"""
Function call for entropy estimation.
Do not change this code
"""


def MI(A, B):
    if len(A) != len(B):
        raise ValueError("A and B must have the same length")
    with open("/tmp/MI_temp.dat", "w+") as tmp:
        for (a, b) in zip(A, B):
            tmp.write("%f %f\n" % (a, b))
    return float(check_output(["./MIhigherdim", "/tmp/MI_temp.dat", "2", "1", "1", "%d" % len(A), "8"]))


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
    max_a = [max(A),max(B),max(E)]
    min_a = [min(A),min(B),min(E)]
    ran = [max_a[0]-min_a[0],max_a[1]-min_a[1],max_a[2]-min_a[2]]
    
    ran = [1 if x==0 else x for x in ran]
    
    #n = [math.log(ran[0],2),math.log(ran[1],2),math.log(ran[2],2)]
    
    m = 2**number_of_bits
    x = numpy.flip(gray_code(number_of_bits),0)  #Array umdrehen, damit Bereichsgrenzen mit vorgabe übereinstimmen

    for i in range(0,len(A)):
        gcode = int(math.floor(float(abs(A[i])-abs(max_a[0]))*m/ran[0])) #Arrayindex(Bereichsgrenze) berechnen
        if gcode == m:  #ran[0]*m /ran[0] anfangen, dann kommt 4 raus, ist aber kein gültiger Index
            gcode= m-1
        bA.append(x[gcode])  #Gray_code an stelle x einfügen

        gcode = int(math.floor(float(abs(B[i])-abs(max_a[1]))*m/ran[1]))
        if gcode == m:
            gcode= m-1
        bB.append(x[gcode])

        gcode = int(math.floor(float(abs(E[i])-abs(max_a[2]))*m/ran[2]))
        if gcode == m:
            gcode= m-1
        bE.append(x[gcode])

    bA = numpy.concatenate(bA,axis=0).tolist() #Array of arrays zum Array of Zahlen machen
    bB = numpy.concatenate(bB,axis=0).tolist()
    bE = numpy.concatenate(bE,axis=0).tolist()
    return (bA,bB,bE)  
    
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
    m_a = numpy.mean(A) #Mittelwert
    m_b = numpy.mean(B)
    m_e = numpy.mean(E)

    std_a = numpy.std(A, ddof=1) #durch n-ddof teilen (ddof=1) std-derivation Berechnen
    std_b = numpy.std(B, ddof=1)
    std_e = numpy.std(E, ddof=1)

    q_a_plus = (m_a + alpha * std_a) #q+ 
    q_b_plus = (m_b + alpha * std_b)
    q_e_plus = (m_e + alpha * std_e)

    q_a_minus = (m_a - alpha * std_a) #q-
    q_b_minus = (m_b - alpha * std_b)
    q_e_minus = (m_e - alpha * std_e)

    #print(q_b_plus,q_b_minus)
    L = []
    i = 0

    #Alice get L
    while i <= len(A)-m:
        if A[i] < q_a_minus:
            x = 0
            #Teste ob weitere m kleiner als q- sind
            for z in range(0,m):
                if A[i+z] >= q_a_minus:
                    x = 1
                    break
            #Wenn es m Werte gab anhängen
            i_start = i
            #immer bis zum letzten Element, welches kleiner als q- ist durchgehen
            while A[i] < q_a_minus and i < len(A)-1:
                i+=1

            #wenn weniger als m Werte unter q- mache die while Schleife weiter
            if x == 1:
                continue
            #Anhängen falls mehr als m Werte unter q-
            app_var = math.floor(float(i_start+i)/2)
            L.append(app_var)
            continue

        #Wie oben nur mit "größer" und q+
        if A[i] > q_a_plus:
            x = 0
            for z in range(0,m):
                if A[i+z] <= q_a_plus:
                    x = 1
                    break
            
            #Wenn es m Werte gab anhängen
            i_start = i
            #immer bis zum letzten Element durchgehen
            while A[i] > q_a_plus and i < len(A)-1:
                i+=1

            if x == 1:
                continue
            app_var = int(math.floor(float(i_start+i)/2))
            L.append(app_var)
            continue

        i+=1
    #print(len(L))

    #Berechne Lschlange
    L_Schlange = []

    #Bob überprüft auf matchings
    for i in L:
        x = 0 
        #Wie im Paper beschrieben ermittele Anfangswert
        start = int(i-math.floor(float(m-2)/2))
        #Wie im Paper beschrieben ermittele Endwert
        end = int(i+math.ceil(float(m-2)/2))
        #Teste ob alle Werte zwischen start und end kleiner als q- sind
        if B[start] < q_b_minus :
            for z in range(0,end-start+1):
                if B[start+z] >= q_b_minus:
                    x = 1
            #Wenn dies der Fall ist hänge i an Lschlange an und leite 1 Bit ab
            if x != 1:
                L_Schlange.append(i)
                bB.append(0)
            continue

        #Teste ob alle Werte zwischen start und end größer als q+ sind
        if B[start] > q_b_plus :
            for z in range(0,end-start+1):
                if B[start+z] <= q_b_minus:
                    x = 1
            #Wenn dies der Fall ist hänge i an Lschlange an und leite 1 Bit ab
            if x != 1:
                L_Schlange.append(i)
                bB.append(1)

    #print(L_Schlange)

    #Alice und Bob leiten bits anhang von L_Schlange ab
    for i in L_Schlange:
        if A[i] > q_a_plus:
            bA.append(1)
        elif A[i] < q_a_minus:
            bA.append(0)


        if E[i] > q_e_plus:
            bE.append(1)
        elif E[i] < q_e_minus:
            bE.append(0)

    return bA, bB, bE  # After implementation, return binary vectors as tuple

