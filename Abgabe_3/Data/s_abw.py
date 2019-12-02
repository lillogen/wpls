import csv
from sys import argv
from utils import *
import math
from argparse import ArgumentParser
args_parser = ArgumentParser()
args_parser.add_argument("-F", type=path, required=True, help="Path to measurement")

args, unknown  = args_parser.parse_known_args()
a = "00124b0001542bf5_00124b0001542c6d_00124b0001542c6d.csv"
b = "00124b0001542c6d_00124b0001542bf5_00124b0001542bf5.csv"
c = "00124b00015735cf_00124b0001542bf5_00124b0001542bf5.csv"
path_ = args.F 

def st_abw(path_):
	mittelwert = 0 
	with open(path_, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ')
		for row in spamreader:
			x = str(row[0].split(";")[1:]).strip("[]'")
			x = int(str(x),10)
			mittelwert=(mittelwert+x)
	
		mittelwert/=spamreader.line_num	
	abweichung = 0
	with open(path_, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ')
		for row in spamreader:
			x = str(row[0].split(";")[1:]).strip("[]'")
			x = int(str(x),10)
			abweichung+= (x-mittelwert)**2
		abweichung/=spamreader.line_num
		abweichung = math.sqrt(abweichung)

	return abweichung,mittelwert

abweichung,mittelwert = st_abw(path_+"/"+a)
print("Alice Mittelwert ist :",mittelwert, " bei einer Standardabweichung von ", abweichung)
abweichung,mittelwert = st_abw(path_+"/"+b)
print("Bob's Mittelwert ist :",mittelwert, " bei einer Standardabweichung von ", abweichung)
abweichung,mittelwert = st_abw(path_+"/"+c)
print("Eve's Mittelwert ist :",mittelwert, " bei einer Standardabweichung von ", abweichung)
