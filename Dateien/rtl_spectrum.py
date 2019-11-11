import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
import numpy as np
from scipy import signal
import pylab as pl
import asyncio
np.set_printoptions(threshold=np.inf)

sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.4e6
sdr.center_freq = 106.6e6
sdr.gain = 20
sdr.bandwith= 500e3
samples = sdr.read_samples(1024*2048)

def first(samples):
	freq, power = signal.welch(samples, sdr.sample_rate, window='hann', nperseg=2048, scaling='spectrum')
	
	plt.plot(np.fft.fft(samples)[2:])
	#print(type(freq))
	#power_sorted = [x for _,x in sorted(zip(freq,power))]
	#freq_sorted = sorted(freq)
	plt.show()
	plt.figure()
	return 0
	#plt.semilogy(freq[int(len(freq)/2):], np.sqrt(power[int(len(freq)/2):]))
	plt.semilogy(freq[int(len(freq)):-1], np.sqrt(power[int(len(freq)):-1]))
	#plt.semilogy(freq[0:int(len(freq)/2)], np.sqrt(power[0:int(len(freq)/2)]))
	plt.semilogy(freq[int(len(freq)):-1], np.sqrt(power[int(len(freq)):-1]))
	
	#plt.semilogy(freq, np.sqrt(power))
	plt.xlabel('frequency [Hz]')
	plt.ylabel('Relative Power')
	plt.show()
	
	#y = signal.triang(2048*100)
	#x = np.correlate(freq,y,mode='full')
	#plt.plot(x)
	#plt.show()

def second(samples):
	pl.psd(samples, NFFT=1048, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6, noverlap=True)
	pl.xlabel('Frequency (MHz)')
	pl.ylabel('Relative power (dB)')
	pl.show()


def fourier_trafo(samples):
	freq, power = signal.welch(samples, sdr.sample_rate, window='hann', nperseg=2048, scaling='spectrum')
	return freq , power

#first(samples)
#second(samples)
async def streaming(freq,power):
    #sdr = RtlSdr()

    async for samples in sdr.stream():
        if sdr.center_freq+sdr.bandwidth>120e6:
        	 return freq,power
        freq1,power1 = fourier_trafo(samples)
        #print(len(freq),len(power))
        freq = np.append(freq,freq1)
        power = np.append(power,power1)
        sdr.center_freq+=500e3
        print(sdr.center_freq)
    
    await sdr.stop()

    # done
    sdr.close()

def py_3():
	freq = []
	power = []
	loop = asyncio.get_event_loop()
	freq,power = loop.run_until_complete(streaming(freq,power))
	
	#print(freq)
	
	plt.semilogy(freq, np.sqrt(power))
	#plt.semilogy(freq[0:int(len(freq)/2)], np.sqrt(power[0:int(len(freq)/2)]))
	
	#plt.semilogy(freq, np.sqrt(power))
	plt.xlabel('frequency [Hz]')
	plt.ylabel('Relative Power')
	plt.show()

first(samples)