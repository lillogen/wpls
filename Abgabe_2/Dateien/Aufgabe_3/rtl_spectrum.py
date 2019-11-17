import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
import numpy as np
from scipy import signal
import pylab as pl

np.set_printoptions(threshold=np.inf)

sdr = RtlSdr()

# configure device
bandwith=500e3
start_freq = 88e6
end_freq = 110e6



sdr.sample_rate = 2.4e6
sdr.center_freq = start_freq
sdr.gain = 20
sdr.bandwith= bandwith
samples = sdr.read_samples(256*2048)

"""
import pylab as pl
import asyncio
async def streaming(freq,power):
    #sdr = RtlSdr()
    fft=[[],[]]
    async for samples in sdr.stream():
        if sdr.center_freq+sdr.bandwidth>end_freq:
        	 return fft
       	z = fourier_trafo_2(samples,1e6,sdr.center_freq)
       	fft[0] = np.append(fft[0],z[0])
       	fft[1] = np.append(fft[1],z[1])
       	#second(samples,1e6,sdr.center_freq)
        #freq1,power1 = fourier_trafo(samples)
        #print(len(freq),len(power))
        #freq = np.append(freq,freq1)
        #power = np.append(power,power1)
        sdr.center_freq+=1000e3
        print(sdr.center_freq)
    
    await sdr.stop()

    # done
    sdr.close()

def first(samples):
	freq, power = signal.welch(samples, sdr.sample_rate, window='hann', nperseg=2048, scaling='spectrum')
	
	plt.plot(np.fft.fft(samples)[2:])
	#print(type(freq))
	#power_sorted = [x for _,x in sorted(zip(freq,power))]
	#freq_sorted = sorted(freq)
	plt.show()
	plt.figure()
	#return 0
	plt.semilogy(freq[int(len(freq)/2):], np.sqrt(power[int(len(freq)/2):]))
	plt.semilogy(freq[0:int(len(freq)/2)], np.sqrt(power[0:int(len(freq)/2)]))
	
	#plt.semilogy(freq, np.sqrt(power))
	plt.xlabel('frequency [Hz]')
	plt.ylabel('Relative Power')
	plt.show()
	
	#y = signal.triang(2048*100)
	#x = np.correlate(freq,y,mode='full')
	#plt.plot(x)
	#plt.show()
"""
def fourier_trafo_2(samples,srate,center):
	freq,power = pl.psd(samples, NFFT=32, Fs=srate, Fc=center, noverlap=False)
	return freq, power
	
	#Bei hohen FFTS sind hässliche peaks zu sehen ... warum?

def fourier_trafo(samples):
	freq, power = signal.welch(samples, sdr.sample_rate, window='hann', nperseg=256, scaling='spectrum')
	return freq,power

def sensing():
	fft=[[],[]] 		#Leeres Freqenz:Power array
	breite = bandwith*2 #step Freqenz setzen
	print(breite)
	while True:	
		if sdr.center_freq > end_freq-breite: 	#bis end_freq erreicht:
			return fft
		samples = sdr.read_samples(128*2048) #samples einlesen
		#z1,z2 = fourier_trafo(samples)		#fft bestimmen
		z1,z2 = fourier_trafo_2(samples,1e6,sdr.center_freq)		#fft bestimmen
		fft[0] = np.append(fft[0],z1+sdr.center_freq)	#x Werte an center-freq anpassen und an PLOT-Array anhängen
		fft[1] = np.append(fft[1],z2)					#Power an plot-array anhängen
		sdr.center_freq+=breite							#Centerfrequenz um Bandbreite*2 erhöhen
		#second(samples,1e6,sdr.center_freq)
		print(sdr.center_freq)
	return -1
"""	
def mull(freq,power):
	samples = []
	fft=[[],[]] 		#Leeres Freqenz:Power array
	breite = bandwith*2 #step Freqenz setzen
	print(breite)
	while sdr.center_freq < end_freq-breite:	
		if (len(samples)>=0):
			samples = np.append(samples,sdr.read_samples(128*2048))
		else:
			samples = sdr.read_samples(128*2048)
		sdr.center_freq+=breite	
	fft[0],fft[1] = fourier_trafo(samples)
	print(len(samples))
	return (fft[0]+(start_freq+end_freq)/2),fft[1]
"""
def py_3(einheit):
	fft = sensing()
	#print(fft[0],fft[1])
	if einheit == 0 :
		plt.plot(fft[0],fft[1]) #zeigt die Stärksten Signale an
		plt.ylabel('Relative Power 10^(db/10)')
	else:
		plt.plot(fft[0],10*np.log10(fft[1])) #Zeigt auch schwächere Signale mit höheren Peaks an, wird aber schnell unübersichtlich
		plt.ylabel('Relative Power dB')
	plt.xlabel('frequency [Hz]')
	plt.show()
	return 0

#second(samples,1e6,start_freq)
#plt.plot(fourier_trafo(samples)[0]+100e6,fourier_trafo(samples)[1])
#plt.show()
py_3(1)
sdr.close()