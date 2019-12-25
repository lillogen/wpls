#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

#########################################
#########################################
##   PhySec-Praktikum Framework 2019   ##
##   Authors: J. Zimmer,               ##
##            J. Brauer                ##
##                                     ##
##   DO NOT CHANGE ANYTHING HERE       ##
##                                     ##
#########################################
#########################################


import matplotlib.pyplot as plt
import time
from utils import *
import numpy
from exercise3 import correlation, quant0

"""
Prolog of each exercise, imports measurements and generates a timestamp
"""
def prolog(args):
    # import measurements and trim them to minimal length
    meas_A = read_measurement(args.A)
    meas_B = read_measurement(args.B)
    meas_E = read_measurement(args.E)

    meas_A, meas_B, meas_E = filter_measurements(meas_A, meas_B, meas_E)

    # determine minimal length
    min_len = min(len(meas_A), len(meas_B), len(meas_E))

    meas_A = meas_A[:min_len]
    meas_B = meas_B[:min_len]
    meas_E = meas_E[:min_len]

    if hasattr(args, "start") and args.start:
        if args.start < min_len:
            meas_A = meas_A[args.start:]
            meas_B = meas_B[args.start:]
            meas_E = meas_E[args.start:]
        else:
            raise ValueError("start is bigger than length of input")

    if hasattr(args, "length") and args.length:
        if args.length <= len(meas_A):
            meas_A = meas_A[:args.length]
            meas_B = meas_B[:args.length]
            meas_E = meas_E[:args.length]
        else:
            raise ValueError("length is bigger than length of remaining input")

    ts = time.strftime("%d_%m_%y_%H_%M_%S")  # timestamp to use during store

    return meas_A, meas_B, meas_E, ts


"""
Executes U3E2
"""
def plot_correlation(args):
    meas_A, meas_B, meas_E, ts = prolog(args)  # prolog

    destination = "output_Ex3/"
    if not os.path.exists(destination):
        os.makedirs(destination)
    if not os.path.exists(os.path.join(destination,"data")):
        os.makedirs(os.path.join(destination,"data"))

    ## Apply correlation function implemented by the student and store plot and correlation coefficients in csv file
    # A <-> B
    correlation_coefficients = map(correlation, chunks(meas_A, args.blocksize), chunks(meas_B, args.blocksize))

    if args.style == "dots":
        dots(correlation_coefficients, "blue", xlabel="Blocks", ylabel="Pearson Correlation $\\rho$ for $A \leftrightarrow B$")
    elif args.style == "line":
        timeplot(correlation_coefficients, "blue", xlabel="Blocks", ylabel="Pearson Correlation $\\rho$ for $A \leftrightarrow B$")
    else:
        print("Illegal argument for style. Using dots instead. For help view documnetation.")
        dots(correlation_coefficients, "blue", xlabel="Blocks", ylabel="Pearson Correlation $\\rho$ for $A \leftrightarrow B$")

    multiple_save(os.path.join(destination, "correlation_AB"))
    store_list(os.path.join(destination, "data/correlation_AB.csv"), correlation_coefficients)
    plt.clf()

    # Apply correlation function implemented by the student and store plot and correlation coefficients in csv file
    # A <-> E
    correlation_coefficients = map(correlation, chunks(meas_A, args.blocksize), chunks(meas_E, args.blocksize))

    if args.style == "dots":
        dots(correlation_coefficients, "red", xlabel="Blocks", ylabel="Pearson Correlation $\\rho$ for $A \leftrightarrow E$")
    elif args.style == "line":
        timeplot(correlation_coefficients, "blue", xlabel="Blocks", ylabel="Pearson Correlation $\\rho$ for $A \leftrightarrow B$")
    else:
        dots(correlation_coefficients, "blue", xlabel="Blocks", ylabel="Pearson Correlation $\\rho$ for $A \leftrightarrow E$")
    
    multiple_save(os.path.join(destination, "correlation_AE"))
    store_list(os.path.join(destination, "data/correlation_AE.csv"), correlation_coefficients)
    plt.clf()


"""
Executes U3A4
"""
def plot_quantizizer(args):
    meas_A, meas_B, meas_E, ts = prolog(args)  # prolog

    Qs = [quant0]

    destination = "output_Ex3/"

    args_out = args.out
    if not args_out:  # TODO check if there are illegal arguments and print error
        print("No output!")  # can't happen since out needs at least one input

    ## Apply selected quantization scheme block-wise

    bA = []
    bB = []
    bE = []
    for pair in zip(chunks(meas_A, args.qsize), chunks(meas_B, args.qsize), chunks(meas_E, args.qsize)):
        tA, tB, tE = Qs[args.quantizer](*pair, args=args)
        bA += tA
        bB += tB
        bE += tE


    if "data" in map(str.lower, args_out):
        ## Store bitstream
        if not os.path.exists(os.path.join(destination,"data")):
            os.makedirs(os.path.join(destination,"data"))
        for b, store_path in zip([bA, bB, bE], [os.path.join(destination, "data/%s_%s.csv" % (i, ts)) for i in["Quantized_ab", "Quantized_ba", "Quantized_ae"]]):
            with open(store_path, "w+") as out:
                out.write("\n".join(["%d" % i for i in b]))

    # Measurement Output:
    if 'plots' in map(str.lower, args_out):
        blockwiseA = chunks(meas_A, args.qsize)
        blockwiseB = chunks(meas_B, args.qsize)
        blockwiseE = chunks(meas_E, args.qsize)
        measure_meansA = []
        measure_meansB = []
        measure_meansE = []
        quantize_A = []

        for i in range(args.plen, 0, -args.qsize):
            try:
                measure_meansA.extend(blockwiseA.next())
                measure_meansB.extend(blockwiseB.next())
                measure_meansE.extend(blockwiseE.next())
            except StopIteration:
            	break

        del measure_meansA[1::2]
        del measure_meansB[1::2]
        del measure_meansE[1::2]


        plot([measure_meansA, measure_meansB, measure_meansE], ["blue", "green", "red"], xlabel="Time", ylabel="Amplitude", legend=["A", "B", "E"], linestyle='-', marker='.')
        multiple_save(os.path.join(destination, "measurement_shortened_%s" % ts))
        plt.clf()

        bA_b = []
        bB_b = []
        bE_b = []

        tA, tB, tE = Qs[args.quantizer](measure_meansA, measure_meansB, measure_meansE, args=args)
        bA_b += tA
        bB_b += tB
        bE_b += tE

        subplots([bA_b, bB_b, bE_b], ["blue", "green", "red"], xlabel="Time", ylabel="Amplitude", legend=["A", "B", "E"], linestyle='-', marker='.', drawstyle='steps-post')
        multiple_save(os.path.join(destination, "quantize_shortened_%s" % ts))
        plt.clf()


# Main
if __name__ == "__main__":
    from argparse import ArgumentParser
    from sys import argv

    args_parser = ArgumentParser()
    args_parser.add_argument("-A", "-a", metavar="PATH_TO_NODE_A", type=path, required=True, help="Path to node A measurement")
    args_parser.add_argument("-B", "-b", metavar="PATH_TO_NODE_B", type=path, required=True, help="Path to node B measurement")
    args_parser.add_argument("-E", "-e", metavar="PATH_TO_NODE_E", type=path, required=True, help="Path to node E measurement")
    args_parser.add_argument("-X", "--excersise", metavar="Number of task", choices=[2, 4], type=int, required=True, help="Number of task (2, 4)")
    args_parser.add_argument("--start", metavar="start sample", type=int, required=False, help="Start evaluation at this sample")
    args_parser.add_argument("--length", metavar="no. of samples", type=int, required=False, help="Only evaluate this number of samples")
    args_parser.add_argument("--style", metavar="STYLE", type=str, required=False, default="dots", help="Select output style - use 'dots' or 'line'")

    args, unknown = args_parser.parse_known_args()

    if args.excersise == 2:
        args_parser.add_argument("--blocksize", metavar="BLOCKLENGTH", type=int, required=False, default=128,help="Blocksize for correlation calculation.")
        
        args = args_parser.parse_args()
        plot_correlation(args)

    elif args.excersise == 4:
        args_parser.add_argument("--qsize", metavar="Q_BLOCKLENGTH", type=int, required=False, default=128,help="Blocksize for quantization")
        args_parser.add_argument("--bits", metavar="BITS_PER_SYMBOL", type=int, required=False, default=2, help="Bits per symbol")
        args_parser.add_argument("--out", metavar="OUTPUT", type=str, nargs='+', required=False,default=["plots", "data"], help="Select output data")
        args_parser.add_argument("--plen", metavar="PLOTLENGTH", type=int, required=False, default=100,help="Determine the legth of the plottet data. Default is 200.")
        args_parser.add_argument("-Q", "--quantizer", metavar="QUANTIZER_NO", choices=[0], type=int,required=True, default=0, help="Which quantizer to use")
        
        args = args_parser.parse_args()
        plot_quantizizer(args)
