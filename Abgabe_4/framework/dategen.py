import csv
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
		abweichung/=(spamreader.line_num-1)
		abweichung = math.sqrt(abweichung)

	return abweichung,mittelwert

def entropie(path_):
	s = []
	entro = 0
	with open(path_, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ')
		for row in spamreader:
			x = str(row[0].split(";")[1:]).strip("[]'")
			x = int(str(x),10)
			s.append(x)
	counter = []
	for i in range(-120,20):
		counter.append(s.count(i))
	len_s = len(s)
	for i in range(0,140):
		pai = counter[i]/len_s
		if counter[i]!=0:
			entro+= -(math.log2(pai)*pai)
	return entro




abweichung,mittelwert = st_abw(path_+"/"+a)
entro = entropie(path_+"/"+a)
print("Alice Mittelwert ist :","%.5f" %mittelwert, "| bei einer Standardabweichung von ", "%.5f" %abweichung, "| die Entropie Beträgt ", "%.5f"%entro)
abweichung,mittelwert = st_abw(path_+"/"+b)
entro = entropie(path_+"/"+b)
print("Bob's Mittelwert ist :","%.5f" %mittelwert, "| bei einer Standardabweichung von ", "%.5f" %abweichung, "| die Entropie Beträgt ", "%.5f"%entro)
abweichung,mittelwert = st_abw(path_+"/"+c)
entro = entropie(path_+"/"+c)
print("Eve's Mittelwert ist :","%.5f" %mittelwert, "| bei einer Standardabweichung von ", "%.5f" %abweichung, "| die Entropie Beträgt ", "%.5f"%entro)

print("&","Mittelwert","&","empirische Standardabweichung","\\\\")
print("\hline")
abweichung,mittelwert = st_abw(path_+"/"+a)
print("Alice","&","%.5f" %mittelwert,"&","%.5f" %abweichung,"\\\\")
abweichung,mittelwert = st_abw(path_+"/"+b)
print("\hline")
print("Bob","&","%.5f" %mittelwert,"&","%.5f" %abweichung,"\\\\")
abweichung,mittelwert = st_abw(path_+"/"+c)
print("\hline")
print("Eve","&","%.5f" %mittelwert,"&","%.5f" %abweichung,"\\\\")

entropie(path_+"/"+a)