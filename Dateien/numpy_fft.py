import matplotlib.pyplot as plt
import numpy as np
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

def bildeinlesen(stelle,file1,plot,type):
	im = np.array(Image.open('Physec_Schriftzug.png'))
	x_achse=im.shape[1]
	y_achse=im.shape[0]
	fsamplerate=x_achse*2 #X-achse als Samplerate Einstellen 
	
	stelle = stelle % y_achse

	arr = np.zeros((y_achse,x_achse), dtype = 'bool')
	
	for i in range(y_achse):
		for x in range(x_achse):
			if ((im[i,x,0]<127) and (im[i,x,1]<127) and (im[i,x,2]<127)):
				arr[i,x]= 1#[0,0,0,255]
			else:
				arr[i,x]= 0 #[255,255,255,255]
	sign = 0
	if type==1:
		sign = fft_real(arr,fsamplerate,x_achse,y_achse,plot,stelle)
	else:
		sign = fft_complex(arr,fsamplerate/2,x_achse,y_achse,plot,stelle)
	
	#im = Image.fromarray(arr)
	#im.show()
	#print(sign)
	s = struct.pack('f'*len(sign), *sign)
	file1.write(s)
	
def fft_real(arr,fsamplerate,x_achse,y_achse,plot,stelle):
	t = np.arange(0,1, 1.0/fsamplerate)
	y = np.sin(2*np.pi*0*t)
	for i in range(x_achse):
		if arr[stelle,i]==1:
			y += np.sin(2*np.pi* i *t)
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
	t = np.arange(0,1, 1.0/fsamplerate)
	y = 0
	#y = np.exp(2*np.pi*0 * t * 1j)
	for i in range(x_achse):
		if arr[stelle,i]==1:
			y += np.exp(2*np.pi* i * t * 1j)
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

file = open("/tmp/trash.bin", "wb")
#for i in range(160,300):
#	print(i)
#	fourier(i,file,0)
#fourier(1,file,1)
#fourier_c(150,file)

#file.close()
for i in range(120,250):
	bildeinlesen(i,file,0,1)
	print(i)
file.close()