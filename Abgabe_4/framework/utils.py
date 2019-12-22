#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#########################################
#########################################
##   PhySec-Praktikum Framework 2018   ##
##   Authors: J. Zimmer,               ##
##            J. Brauer                ##
##                                     ##
##   DO NOT CHANGE ANYTHING HERE       ##
##                                     ##
#########################################
#########################################

from math import log
import os
import matplotlib.pyplot as plt
import threading

### Utility Functions ###

"""
Converts a given integer x to its binary representation as an array of {0, 1}^n.
LSB is stored at index 0.
If integer's binary length is >n, all leading bits will be dismissed.
If integer's binary length is <n, it will be padded with 0.
If n == -1, returned array will always have binary length of x.
"""


def de2bi(x, n=-1):
    i = 0
    vec = []
    while x != 0:
        vec.append(x & 1)  # mask out LSB
        i += 1
        if i == n and n != -1:  # if length is given, check if we already reached it
            break
        x = x >> 1  # remove lsb

    if n != -1:  # pad with leading zeros
        while i < n:
            vec.append(0)
            i += 1

    return vec


"""
Converts a given binary vector to its integer representation.
LSB should be stored at index 0.
If MSB at index zero, please set MSB_at_zero to True.
"""


def bi2de(vec, MSB_at_zero=False):
    x = 0

    if MSB_at_zero:  # if MSB at index 0, reverse the vector
        rev = reversed
    else:  # else return the vector unchanged
        rev = lambda x: x

    for i, b in rev(enumerate(vec)):
        x |= (1 << i)
    return x


"""
Returns all Gray-code symbols of size n in ascending order as array of binary vectors of length n.
"""


def gray_code(n):
    return [de2bi((x ^ (x >> 1)), n) for x in range(1 << n)]


"""
Returns log2(x)
"""


def log2(x):
    return log(x) / log(2)


### Utility Functions for internal use only###

"""
Returns a normalitzed path from a string.
"""


def path(s):
    return os.path.realpath(os.path.normpath(s))


"""
Starts function in new thread.
"""


def in_parallel(fnc):
    threading.Thread(target=fnc).start()


"""
Yields n-sized chunks from l, rest is dropped
"""


def chunks(l, n):
    for i in range(0, len(l), n):
        if i + n <= len(l):  # skip short chunk at the end
            yield list(l[i:i + n])


"""
Reads measurement from file.
"""


def read_measurement(path):
    measurement = [[], []]
    # noinspection PyArgumentEqualDefault
    with open(path, "r") as i:
        for line in i:
            sync, val = line.split(';')
            measurement[0].append(int(sync.strip()))
            measurement[1].append(int(val.strip()))
    return measurement


"""
Filters tuples which have synchronouse synch fields
"""


def filter_measurements(*args):
    ret = [[] for m in args]

    new_s = 0

    while True:
        c = False
        b = False

        if len(args[0][0]) == 0:
            break

        s = args[0][0][0]  # get first synch

        if new_s > s:
            s = new_s

        for m in args:
            if len(m[0]) == 0:
                b = True
                break
            while m[0][0] < s:
                del m[0][0]
                del m[1][0]
                if len(m[0]) == 0:
                    b = True
                    break
        if b:
            break

        for m in args:
            if m[0][0] > s:
                new_s = m[0][0]
                c = True
                break

        if c:
            continue

        for i, m in enumerate(args):
            ret[i].append(m[1][0])
            del m[0][0]
            del m[1][0]

    return ret


"""
    Stores list of numbers in ascii line by line.
"""


def store_list(saveto, l):
    if not os.path.isdir(os.path.dirname(saveto)):
        os.makedirs(os.path.dirname(saveto))
    with open("%s" % saveto, "w+") as dest:
        for element in l:
            dest.write("%s\n" % str(element))


"""
Saves plot in multiple formats
"""


def multiple_save(saveto, formats=None):
    if formats is None:
        formats = ['png']
    if 'show' in saveto:
        plt.show()
        return
    if not os.path.isdir(os.path.dirname(saveto)):
        os.makedirs(os.path.dirname(saveto))
    for form in formats:
        saveto_f = "%s.%s" % (saveto, form)
        plt.savefig(saveto_f)


"""
Set labels and limits of a plot
"""


def label_lim(xlim=None, ylim=None, xlabel=None, ylabel=None):
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
        plt.gcf().subplots_adjust(bottom=0.15)


"""
Plot data as colored dots
"""


def dots(data, colors, xlim=None, ylim=None, xlabel=None, ylabel=None):
    if not isinstance(data[0], list):  # if only one dataset is given
        data = [data]
        colors = [colors]

    for d, c in zip(data, colors):  # plot the dots
        plt.plot(d, linestyle='none', marker='o', markerfacecolor=c, alpha=.5)

    label_lim(xlim, ylim, xlabel, ylabel)  # set labels and limits


"""
Plot data as time/amplitude graph
"""


def timeplot(data, colors, xlim=None, ylim=None, xlabel=None, ylabel=None):
    if not isinstance(data[0], list):  # if only one dataset is given
        data = [data]
        colors = [colors]

    for d, c in zip(data, colors):  # plot the dots
        plt.plot(d, linestyle='-', marker='.', color=c, markerfacecolor=c, alpha=.5)

    label_lim(xlim, ylim, xlabel, ylabel)  # set labels and limits


def plot(data, colors, xlim=None, ylim=None, xlabel=None, ylabel=None, linestyle='none', marker='o', legend=[],
         drawstyle='default'):
    if not isinstance(data[0], list):
        data = [data]
        colors = [colors]
        legend = [legend]
    if len(legend) == len(data):
        for d, c, l in zip(data, colors, legend):  # plot
            plt.plot(d, linestyle=linestyle, marker=marker, markerfacecolor=c, color=c, alpha=.5, drawstyle=drawstyle,
                     label=l)
        ax = plt.subplot(111)
        ax.legend()
    else:
        for d, c in zip(data, colors):  # plot
            plt.plot(d, linestyle=linestyle, marker=marker, markerfacecolor=c, alpha=.5, drawstyle=drawstyle)

    label_lim(xlim, ylim, xlabel, ylabel)  # set labels and limits


'''
Only works for 3 Datasets given!
'''


def subplots(data, colors, xlim=None, ylim=None, xlabel=None, ylabel=None, linestyle='none', marker='o', legend=[],
             drawstyle='default'):
    if not isinstance(data[0], list):
        data = [data]
        colors = [colors]
        legend = [legend]
    fig = plt.figure()
    i = 311
    if len(legend) == len(data):
        for d, c, l in zip(data, colors, legend):  # plot
            axis = fig.add_subplot(i)
            i += 1
            axis.plot(d, linestyle=linestyle, marker=marker, color=c, alpha=.5, drawstyle=drawstyle, label=l)
            axis.set_ylim(-0.1, 1.1)
            axis.legend()
    else:
        for d, c in zip(data, colors):  # plot
            axis = fig.add_subplot(i)
            i += 1
            axis.plot(d, linestyle=linestyle, marker=marker, markerfacecolor=c, alpha=.5, drawstyle=drawstyle)

    label_lim(xlim, ylim, xlabel, ylabel)  # set labels and limits


"""
Throw not yet implemented exception.
"""


def not_yet_implemented(s):
    raise NotImplementedError("Implementation mising: %s\n" % s)
