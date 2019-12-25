#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
 Physec Praktikum								
 Author: Jan Thoma, 2017							


 Use this programm to concatenate your measurement data form Assignemnet 3.
 The data in the first table will be the first in your output list. 
'''
import os

def concatenate(args):
	pathlist=[args.A, args.B, args. E]
	path = ["1_ohneBwg_A_B","2_mitBwg_A_B", "3_a_mitBwg_A_B", "3_a_ohneBwg_A_B", "3_b_mitBwg_A_B","3_b_ohneBwg_A_B","4_mitBwg_A_B", "5_mitBwg_A_B"]
	files = ["00124b0001542bf5_00124b0001542c6d_00124b0001542c6d.csv", "00124b0001542c6d_00124b0001542bf5_00124b0001542bf5.csv", "00124b00015735cf_00124b0001542bf5_00124b0001542bf5.csv"]
	A = []
	B = []
	C = []
	end = [A,B,C]
	for i in range(3):
		for x in path:
			end[i].append(x+"/"+files[i])
	print(end)
	pathlist = end
	if not os.path.exists("output/"):
		os.makedirs("output/")
	for i in range(3):
		if pathlist[i]: #check if list is not empty 
			fout = open("output/"+numToNode(i)+".csv", "w+")
			for path in pathlist[i]:	
				for line in open(path):
					fout.write(line)
			fout.close()		
def numToNode(i):
	switcher={
		0: "A",
		1: "B",
		2: "E",
	}
	return switcher.get(i,"noName")
	

#Main
if __name__=="__main__":
	from argparse import ArgumentParser
	from sys import argv
	args_parser= ArgumentParser()
	args_parser.add_argument("-A", "-a", metavar="Path to Input files from node A", nargs='+', type=str, required=False, help="Select your input files from node A. You select multiple files by seperating them with a sace.")
	args_parser.add_argument("-B", "-b", metavar="Path to Input files from node B", nargs='+', type=str, required=False, help="Select your input files from node B. You select multiple files by seperating them with a sace.")
	args_parser.add_argument("-E", "-e", metavar="Path to Input files from node E", nargs='+', type=str, required=False, help="Select your input files from node E. You select multiple files by seperating them with a sace.")
	args = args_parser.parse_args()
	concatenate(args);


