import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from PIL import Image, ImageFilter 
import struct
np.set_printoptions(threshold=np.inf)

def test():
	Fs = 150.0; 
	t = np.arange(0,1, 1.0/Fs)   
	y = np.sin(2*np.pi*10*t)
	y = y+np.sin(2*np.pi*15*t)
	y = y+np.sin(2*np.pi*20*t)
	y = y+np.sin(2*np.pi*21*t)
	y = y+np.sin(2*np.pi*21*t)
	y = y+np.sin(2*np.pi*30*t)
	y = y+np.sin(2*np.pi*30*t)
	y = y+np.sin(2*np.pi*30*t)
	n = len(y)
	
	Y = np.fft.fft(y)/n
	Y = Y[range(int(n/2))]
	
	# Plotting
	fig, ax = plt.subplots(2, 1)
	ax[0].plot(t,y)
	ax[1].plot(abs(Y),'r')
	plt.show()

def konturen():
	im1 = Image.open('baudlineStern.png')
	im2 = im1.filter(ImageFilter.CONTOUR)   
	im2.show(im2)

def bildeinlesen(file1,plot,type,mini,maxi):
	im = np.array(Image.open('baudlineStern.png'))
	x_achse=im.shape[1]
	y_achse=im.shape[0]
	fsamplerate=x_achse*2 #X-achse als Samplerate Einstellen 
	
	maxi = maxi % y_achse
	if maxi==0:
		mini = 0
		maxi = y_achse
	arr = np.zeros((y_achse,x_achse), dtype = 'bool')
	##aus der Funktion auslagern:
	for i in range(y_achse):
		for x in range(x_achse):
			if ((im[i,x,0]<127) and (im[i,x,1]<127) and (im[i,x,2]<127)):
				arr[i,x]= 1#[0,0,0,255]
			else:
				arr[i,x]= 0 #[255,255,255,255]
	###
	for i in range(mini,maxi):
		sign = 0
		if type==0:
			print("Using Real fft")
			sign = fft_real(arr,fsamplerate,x_achse,y_achse,plot,i)
		elif type==1:
			print("Using Complex fft")
			sign = fft_complex(arr,fsamplerate,x_achse,y_achse,plot,i)
		elif type==2:
			print("Using Numpy fft")
			sign = np.fft.ifft(arr[i])*10e50
		#im = Image.fromarray(arr)
		#im.show()
		#print(sign)
		s1 = bytes(0)
		s2 = bytes(0)
		for i in range(len(sign)):
			s1 += struct.pack('f',sign[i].real)
			s1 += struct.pack('f',sign[i].imag)

		file1.write(s1)
		#print(sign)
	
def fft_real(arr,fsamplerate,x_achse,y_achse,plot,stelle):
	t = np.arange(0,1, 2.0/fsamplerate)
	y = np.sin(2*np.pi*0*t)
	for i in range(x_achse):
		if arr[stelle,i]==1:
			y += np.sin(2*np.pi* i *t)*10e100
	if plot == 1:
		n = len(y)
		Y = np.fft.fft(y)/(n)
		Y = Y[range(int(n/2))]
		#Plotting
		fig, ax = plt.subplots(2, 1)
		ax[0].plot(t,y)
		ax[1].plot(abs(Y),'r')
		plt.show()
	return y

def fft_complex(arr,fsamplerate,x_achse,y_achse,plot,stelle):
	t = np.arange(0,1, 2.0/fsamplerate)
	y = np.exp(2*np.pi*0 * t * 1j)
	for i in range(x_achse):
		if arr[stelle,i]==1:
			y += np.exp(2*np.pi* (i-x_achse/2) * t * 1j)*10e50
	if plot == 1:
		n = len(y)
		Y = np.fft.fft(y)/n
		Y = Y[range(int(n))]
		#Plotting
		fig, ax = plt.subplots(2, 1)
		ax[0].plot(t,y)
		ax[1].plot(abs(Y),'r')
		plt.show()
	return y

file = open("/tmp/signal.wav", "wb")

bildeinlesen(file,0,1,0,0)

file.close()

#test()