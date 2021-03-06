#!/usr/bin/env python3
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


import time
import os
from exercise4 import ber, MI, quant0, quant1, quant2, correlation
import utils as ut
from itertools import repeat
"""
Prolog of each exercise, imports measurements and generates a timestamp
"""


def prolog(args):
    # import measurements and trim them to minimal length
    meas_A = ut.read_measurement(args.A)
    meas_B = ut.read_measurement(args.B)
    meas_E = ut.read_measurement(args.E)

    meas_A, meas_B, meas_E = ut.filter_measurements(meas_A, meas_B, meas_E)

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


def plot_correlation(meas_A, meas_B, meas_E, ts, args):
    ## Apply correlation function implemented by the student and store plot and correlation coefficients in csv file
    # A <-> B

    correlation_coefficients = list(map(correlation, ut.chunks(meas_A, args.size), ut.chunks(meas_B, args.size)))

    if args.style == "dots":
        ut.dots(correlation_coefficients, "blue", xlabel="Blocks",
             ylabel="Pearson Correlation $\\rho$ for $A \leftrightarrow B$")
    elif args.style == "line":
        ut.timeplot(correlation_coefficients, "blue", xlabel="Blocks",
                 ylabel="Pearson Correlation $\\rho$ for $A \leftrightarrow B$")
    else:
        print("Illegal argument for style. Using dots instead. For help view documnetation.")
        ut.dots(correlation_coefficients, "blue", xlabel="Blocks",
             ylabel="Pearson Correlation $\\rho$ for $A \leftrightarrow B$")

    ut.multiple_save(os.path.join(destination, "correlation_AB_"))
    ut.store_list(os.path.join(destination, "data/correlation_AB.csv"), correlation_coefficients)
    ut.plt.clf()

    # Apply correlation function implemented by the student and store plot and correlation coefficients in csv file
    # A <-> E
    correlation_coefficients = list(map(correlation, ut.chunks(meas_A, args.size), ut.chunks(meas_E, args.size)))

    if args.style == "dots":
        ut.dots(correlation_coefficients, "red", xlabel="Blocks",
             ylabel="Pearson Correlation $\\rho$ for $A \leftrightarrow E$")
    elif args.style == "line":
        ut.timeplot(correlation_coefficients, "blue", xlabel="Blocks",
                 ylabel="Pearson Correlation $\\rho$ for $A \leftrightarrow B$")
    else:
        ut.dots(correlation_coefficients, "blue", xlabel="Blocks",
             ylabel="Pearson Correlation $\\rho$ for $A \leftrightarrow E$")

    ut.multiple_save(os.path.join(destination, "correlation_AE"))
    ut.store_list(os.path.join(destination, "data/correlation_AE.csv"), correlation_coefficients)
    ut.plt.clf()


def apply_quantizizer(meas_A, meas_B, meas_E, args):
    Qs = [quant0, quant1, quant2]

    bA = []
    bB = []
    bE = []
    for pair in zip(ut.chunks(meas_A, args.size), ut.chunks(meas_B, args.size), ut.chunks(meas_E, args.size)):
        bA, bB, bE = (arr + val for arr, val in zip((bA, bB, bE), (Qs[args.quantizer](*pair, args=args))))

    return bA, bB, bE


def plot_quantizizer(meas_A, meas_B, meas_E, ts, args):
    args_out = args.out
    bA, bB, bE = apply_quantizizer(meas_A, meas_B, meas_E, args)

    if "data" in map(str.lower, args_out):
        ## Store bitstream
        for b, store_path in zip([bA, bB, bE], [os.path.join(destination, "data/%s.csv" % (i)) for i in
                                                ["Quantized_ab_{}".format(args.quantizer), "Quantized_ba_{}".format(args.quantizer), "Quantized_ae_{}".format(args.quantizer)]]):
            with open(store_path, "w+") as out:
                out.write("\n".join(["%d" % i for i in b]))

    # Just plotting every second point to increase readability of diagrams.
    if 'plots' in map(str.lower, args_out):
        measure_shortedA = []
        measure_shortedB = []
        measure_shortedE = []

        for pair in zip(ut.chunks(meas_A, args.size), ut.chunks(meas_B, args.size), ut.chunks(meas_E, args.size)):
            measure_shortedA, measure_shortedB, measure_shortedE = (arr + val[::2] for arr, val in zip(
                (measure_shortedA, measure_shortedB, measure_shortedE), pair))
        quant_shortedA, quant_shortedB, quant_shortedE = apply_quantizizer(measure_shortedA, measure_shortedB,
                                                                           measure_shortedE, args)

        ut.plot([measure_shortedA, measure_shortedB, measure_shortedE], ["blue", "green", "red"], xlabel="Time",
             ylabel="Amplitude", legend=["A", "B", "E"], linestyle='-', marker='.')
        ut.multiple_save(os.path.join(destination, "measurement_shortened"))
        ut.plt.clf()

        ut.subplots([quant_shortedA, quant_shortedB, quant_shortedE], ["blue", "green", "red"], xlabel="Time",
                 ylabel="Amplitude", legend=["A", "B", "E"], linestyle='-', marker='.', drawstyle='steps-post')
        ut.multiple_save(os.path.join(destination, "quantize_shortened_Quant_{}".format(args.quantizer) ))
        ut.plt.clf()


def plot_ber(meas_A, meas_B, meas_E, ts, args):
    bA, bB, bE = apply_quantizizer(meas_A, meas_B, meas_E, args)

    ## Apply BER function implemented by the student and store plot and csv file
    ber_AB = list(map(ber, ut.chunks(bA, args.size), ut.chunks(bB, args.size)))
    ber_AE = list(map(ber, ut.chunks(bA, args.size), ut.chunks(bE, args.size)))

    if "data" in map(str.lower, args.out):
        ut.store_list(os.path.join(destination, "data/ber_AE_Quant_{}.csv".format(args.quantizer) ), ber_AE)
        ut.store_list(os.path.join(destination, "data/ber_AB_Quant_{}.csv".format(args.quantizer) ), ber_AB)

    if 'plots' in map(str.lower, args.out):
        func = ut.timeplot if args.style == "line" else ut.dots

        func(ber_AB, "blue", xlabel="Blocks", ylabel="Bit Error Rate $\\rho$ for $A \leftrightarrow B$")
        ut.multiple_save(os.path.join(destination, "ber_AB_Quant_{}".format(args.quantizer) ))
        ut.plt.clf()
        func(ber_AE, "red", xlabel="Blocks", ylabel="Bit Error Rate $\\rho$ for $A \leftrightarrow E$")
        ut.multiple_save(os.path.join(destination, "ber_AE_Quant_{}".format(args.quantizer) ))
        ut.plt.clf()


def plot_entropy(meas_A, meas_B, meas_E, ts, args):
    # A <-> A
    ee_A = list(map(MI, ut.chunks(meas_A, args.size), ut.chunks(meas_A, args.size), repeat(args.pathto) ))
    ee_B = list(map(MI, ut.chunks(meas_B, args.size), ut.chunks(meas_B, args.size), repeat(args.pathto) ))
    ee_E = list(map(MI, ut.chunks(meas_E, args.size), ut.chunks(meas_E, args.size), repeat(args.pathto) ))
    if "data" in map(str.lower, args.out):
        ut.store_list(os.path.join(destination, "data/h_A.csv"), ee_A)
        ut.store_list(os.path.join(destination, "data/h_B.csv"), ee_B)
        ut.store_list(os.path.join(destination, "data/h_E.csv"), ee_E)

    if 'plots' in map(str.lower, args.out):
        func = ut.timeplot if args.style == "line" else ut.dots

        func(ee_A, "blue", xlabel="Blocks", ylabel="Entropy(A)")
        ut.multiple_save(os.path.join(destination, "Entropy_A"))
        ut.plt.clf()

        func(ee_B, "green", xlabel="Blocks", ylabel="Entropy(B)")
        ut.multiple_save(os.path.join(destination, "Entropy_B"))
        ut.plt.clf()

        func(ee_E, "red", xlabel="Blocks", ylabel="Entropy(E)")
        ut.multiple_save(os.path.join(destination, "Entropy_E"))
        ut.plt.clf()
    return


def plot_mi(meas_A, meas_B, meas_E, ts, args):
    # A <-> B
    mi_AB = list(map(MI, ut.chunks(meas_A, args.size), ut.chunks(meas_B, args.size), repeat(args.pathto) ))
    mi_AE = list(map(MI, ut.chunks(meas_A, args.size), ut.chunks(meas_E, args.size), repeat(args.pathto) ))
    mi_BA = list(map(MI, ut.chunks(meas_B, args.size), ut.chunks(meas_A, args.size), repeat(args.pathto) ))
    if "data" in map(str.lower, args.out):
        ut.store_list(os.path.join(destination, "data/mi_AB.csv" ), mi_AB)
        ut.store_list(os.path.join(destination, "data/mi_AE.csv" ), mi_AE)
        ut.store_list(os.path.join(destination, "data/mi_BE.csv" ), mi_BA)

    if 'plots' in map(str.lower, args.out):
        func = ut.timeplot if args.style == "line" else ut.dots

        func(mi_AB, "blue", xlabel="Blocks", ylabel="MI for $A \leftrightarrow B$")
        ut.multiple_save(os.path.join(destination, "mutal_information_AB"))
        ut.plt.clf()

        func(mi_AE, "red", xlabel="Blocks", ylabel="MI for $A \leftrightarrow E$")
        ut.multiple_save(os.path.join(destination, "mutal_information_AE"))
        ut.plt.clf()

        func(mi_BA, "green", xlabel="Blocks", ylabel="MI for $B \leftrightarrow A$")
        ut.multiple_save(os.path.join(destination, "mutal_information_BA"))
        ut.plt.clf()
    return


# Main
if __name__ == "__main__":
    from argparse import ArgumentParser

    args_parser = ArgumentParser()

    # Required parameter
    args_parser.add_argument("-A", "-a", metavar="PATH_TO_NODE_A", type=ut.path, required=True,
                             help="Path to node A measurement")
    args_parser.add_argument("-B", "-b", metavar="PATH_TO_NODE_B", type=ut.path, required=True,
                             help="Path to node B measurement")
    args_parser.add_argument("-E", "-e", metavar="PATH_TO_NODE_E", type=ut.path, required=True,
                             help="Path to node E measurement")

    args_parser.add_argument("-X", "--excercise", metavar="Number of task", choices=[1, 2, 3, 4], type=int,
                             required=True, nargs='+',
                             help="Number of task (1,2,3,4)")

    # Optional parameters. If not set, default values will be used

    args_parser.add_argument("--start", metavar="start sample", type=int, required=False,
                             help="Start evaluation at this sample")
    args_parser.add_argument("--length", metavar="no. of samples", type=int, required=False,
                             help="Only evaluate this number of samples")
    args_parser.add_argument("--style", metavar="STYLE", type=str, required=False, default="dots",
                             help="Select output style - use 'dots' or 'line'")
    args_parser.add_argument("--size", metavar="BLOCKSIZE", type=int, required=False, default=128,
                             help="Blocksize for calculation")
    args_parser.add_argument("--out", metavar="OUTPUT", type=str, nargs='+', required=False, default=["plots", "data"],
                             help="Select output data")
    args_parser.add_argument("--bits", metavar="BITS_PER_SYMBOL", type=int, required=False, default=2,
                             help="Bits per symbol")
    args_parser.add_argument("-Q", "--quantizer", metavar="QUANTIZER_NO", choices=[0, 1, 2], type=int,
                             required=False, default=0, help="Which quantizer to use")
    args_parser.add_argument("--alpha", metavar="ALPHA", type=float, required=False, default=0.5, help="Alpha")
    args_parser.add_argument("--m", metavar="M", type=int, required=False, default=3,
                             help="Consecutive number of sample per bits (has to be odd, otherwise m = m -1)")
    args_parser.add_argument("--pathto", metavar="PA", type=str, required=False, default="Abgabe_4/framework/",
                             help="Path to executable file MIhigherdim")

    args = args_parser.parse_args()
    destination = "output_Ex4/"
    if not os.path.exists(destination):
        os.makedirs(destination)
    if not os.path.exists(os.path.join(destination, "data")):
        os.makedirs(os.path.join(destination, "data"))

    meas_A, meas_B, meas_E, ts = prolog(args)  # prolog

    if 1 in args.excercise:
        plot_correlation(meas_A, meas_B, meas_E, ts, args)
    
    if 2 in args.excercise:
        plot_quantizizer(meas_A, meas_B, meas_E, ts, args)

    if 3 in args.excercise:
        plot_ber(meas_A, meas_B, meas_E, ts, args)

    if 4 in args.excercise:
        plot_entropy(meas_A, meas_B, meas_E, ts, args)
        plot_mi(meas_A, meas_B, meas_E, ts, args)
