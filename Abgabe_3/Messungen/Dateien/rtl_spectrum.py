import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
import numpy as np
from scipy import signal
import pylab as pl
import asyncio

np.set_printoptions(threshold=np.inf)

sdr = RtlSdr()

# configure device
start_freq = 100e6
end_freq = 200e6
sdr.sample_rate = 2.4e6
sdr.center_freq = start_freq
sdr.gain = 20
sdr.bandwith= 500e3
samples = sdr.read_samples(256*2048)

async def streaming(freq,power):
    #sdr = RtlSdr()
    fft=[[],[]]
    async for samples in sdr.stream():
        if sdr.center_freq+sdr.bandwidth>end_freq:
        	 return fft
       	z = second(samples,1e6,sdr.center_freq)
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

def second(samples,srate,center):
	x = pl.psd(samples, NFFT=256, Fs=srate/1e6, Fc=center/(1e6), noverlap=False)
	return x
	#Bei hohen FFTS sind hässliche peaks zu sehen ... warum?
	#print(x)
	#pl.xlabel('Frequency (MHz)')
	#pl.ylabel('Relative power (dB)')
	#pl.show()


def fourier_trafo(samples):
	freq, power = signal.welch(samples, sdr.sample_rate, window='hann', nperseg=256, scaling='spectrum')
	return freq , power


def no_async(freq,power):
	fft=[[],[]]
	while True:
		if sdr.center_freq > end_freq:
			return fft
		samples = sdr.read_samples(128*2048)
		z = second(samples,1e6,sdr.center_freq)
		fft[0] = np.append(fft[0],z[0])
		fft[1] = np.append(fft[1],z[1])
		sdr.center_freq+=1e6
		#second(samples,1e6,sdr.center_freq)
		print(sdr.center_freq)


def py_3():
	freq = []
	power = []
	#loop = asyncio.get_event_loop()
	#fft = loop.run_until_complete(streaming(freq,power))
	fft = no_async(freq,power)
	print(fft[0],fft[1])
	
	plt.plot(fft[1],fft[0])
	plt.show()
	return 
	plt.semilogy(freq, np.sqrt(power))
	#plt.semilogy(freq[0:int(len(freq)/2)], np.sqrt(power[0:int(len(freq)/2)]))
	
	#plt.semilogy(freq, np.sqrt(power))
	plt.xlabel('frequency [Hz]')
	plt.ylabel('Relative Power')
	plt.show()

#second(samples,1e6,start_freq)
plt.plot(fourier_trafo(samples)[0]+100e6,fourier_trafo(samples)[1])
plt.show()
#py_3()
#sdr.stop()
#sdr.close()