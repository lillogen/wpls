import matplotlib.pyplot as plt
from rtlsdr import *
import numpy as np
from scipy import signal

sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.4e6
sdr.center_freq = 106.6e6
sdr.gain = 20
sdr.bandwith= 500e3

samples = sdr.read_samples(256*2048)

freq, power = signal.welch(samples, sdr.sample_rate, window='hann', nperseg=2048, scaling='spectrum')

power_sorted = [x for _,x in sorted(zip(freq,power))]
freq_sorted = sorted(freq)

plt.figure()

plt.semilogy(freq[len(freq)/2:], np.sqrt(power[len(freq)/2:]))
plt.semilogy(freq[0:len(freq)/2], np.sqrt(power[0:len(freq)/2]))

#plt.semilogy(freq, np.sqrt(power))
plt.xlabel('frequency [Hz]')
plt.ylabel('Relative Power')
plt.show()

