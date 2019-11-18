import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageFilter 
from struct import *
import random
import cmath

def bildeinlesen(file1,plot,type,mini,maxi):
	im = np.array(Image.open('Bilder/Physec_Schriftzug.png'))
	#im = np.array(Image.open('baudlineStern.png'))
	#im = np.array(Image.open('Bilder/Donald-Trump.jpg'))
	x_achse=im.shape[1]
	y_achse=im.shape[0]
	fsamplerate=x_achse*2 #X-achse als Samplerate Einstellen 
	
	maxi = maxi % y_achse
	if maxi==0:
		mini = 0
		maxi = y_achse
	arr = np.zeros((y_achse,x_achse), dtype = 'bool')
	for i in range(y_achse):
		for x in range(x_achse):
			if ((im[i,x,0]<127) and (im[i,x,1]<127) and (im[i,x,2]<127)):
				arr[i,x]= 1#[0,0,0,255]
			else:
				arr[i,x]= 0 #[255,255,255,255]
	#ifft_complex(arr,fsamplerate,x_achse,y_achse,1,150)
	#im = Image.fromarray(arr)
	#im.show()
	for i in range(mini,maxi):
		sign = 0
		print (i+1," of ", maxi)
		if type==1:
			#print("Using Complex fft")
			y1,y2 = ifft_complex(arr,fsamplerate,x_achse,y_achse,plot,i)
		s1 = bytes(0)

		new_array_cause_python2_sucks = []
		for h in range(len(y1)):
			new_array_cause_python2_sucks.append(y2[h])
			new_array_cause_python2_sucks.append(y1[h])
			#s1 += str((pack('f',y2[h]) + pack('f',y1[h]))) ging aus irgenteinem Grund in PY2 nicht bei complexn werten ist der auch grundlos immer abgeschissen
			#print (pack('f',y2[h]))
		s1 = pack('f'*len(new_array_cause_python2_sucks), *new_array_cause_python2_sucks)
		#print sign
		file1.write(s1)

def ifft_complex(arr,fsamplerate,x_achse,y_achse,plot,stelle):
	scale = 1   #hherer Wert, hhere Genauigkeit, aber auch mehr Rechenleistung
	t = np.arange(0,1, 1.0/(x_achse*scale))
	y1 = np.zeros(x_achse*scale)
	y2 = np.zeros(x_achse*scale)
	for i in range(x_achse):
		if arr[stelle,i]==1:
			#rand = random.random() *2*np.pi* (i-x_achse/2)
			rand = 0
			y1 += np.sin(2*np.pi* (scale*(i-x_achse/2)) * (t+rand)) #imag
			y2 += np.cos(2*np.pi* (scale*(i-x_achse/2)) * (t+rand)) #real
	if plot == 1:
		n = len(y)
		Y = np.fft.fft(y)/n
		#Y = Y[range(int(n))]
		fig, ax = plt.subplots(2, 1)
		ax[0].plot(t,y)
		ax[1].plot(abs(Y),'r')
		plt.show()
	return y1,y2

file = open("/tmp/signal.raw", "wb")

bildeinlesen(file,0,1,0,0) 

file.close()
