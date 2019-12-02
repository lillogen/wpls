import csv
from sys import argv
from utils import *
import math
from argparse import ArgumentParser
args_parser = ArgumentParser()
args_parser.add_argument("-F", type=path, required=True, help="Path to measurement")

args, unknown  = args_parser.parse_known_args()

mittelwert = 0 

with open(args.F, 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ')
	for row in spamreader:
		x = str(row[0].split(";")[1:]).strip("[]'")
		x = int(str(x),10)
		mittelwert=(mittelwert+x)

	mittelwert/=spamreader.line_num
	print(mittelwert)

abweichung = 0
with open(args.F, 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ')
	for row in spamreader:
		x = str(row[0].split(";")[1:]).strip("[]'")
		x = int(str(x),10)
		abweichung+= (x-mittelwert)**2
	abweichung/=spamreader.line_num
	abweichung = math.sqrt(abweichung)

print("Der Mittelwert ist :",mittelwert, " bei einer Standardabweichung von ", abweichung)