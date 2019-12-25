import numpy as np
signal1 = open("/home/bschlueter/University/Semester_3/WPLS/Abgabe_1/Dateien/Funk_2/auto_zu_bin.wav","r")
signal2 = open("/home/bschlueter/University/Semester_3/WPLS/Abgabe_1/Dateien/Funk_2/auto_auf_bin_1.wav","r")
signal3 = open("/home/bschlueter/University/Semester_3/WPLS/Abgabe_1/Dateien/Funk_2/auto_koff_bin.wav","r")

#np.set_printoptions(threshold=np.inf)
def demod(signal):
	x = np.fromfile(signal,dtype=np.int8)
	#print(x)

	endarray=[]

	count = 0
	for i in range(2,len(x)):
		#print(x[i])
		if x[i]==x[i-1]:
			count+=1
		else:
			if x[i-1]==0:
				endarray.append(-count)
			else:
				endarray.append(count)
			count = 1

	#Ab hier ist es Codierungssache
	#print(endarray)
	sta=""
	for i in range(0,len(endarray)):
		if (endarray[i]>50 and endarray[i] < 100):
			endarray[i]="10"
			sta+="0"
			continue
		if(endarray[i] > 100):
			endarray[i]="11"
			sta+="1"
			continue
		if endarray[i]< 100:
			endarray[i]="00"
			continue
		endarray[i]="01"

	#print(endarray)
	string = ''.join(endarray)
	print(hex(int(string,2)))
	#print(sta)
	print(hex(int(sta,2)))

demod(signal1)
demod(signal2)
demod(signal3)

#response = [string[i:i+8] for i in range(0, len(string), 8)]
#for i in range(0,len(response)):
#	response[i]=hex(int(response[i],2))
#print(response[1:-1])