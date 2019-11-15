import math

freq = 1e9
r = 120e3

db = 20*math.log10(r*freq*4*math.pi/299792458)

#print(db)


freq_1 = math.pow(10,103/20)*299792.458/(1*10**9*4*math.pi)
print(freq_1)
print(299792.458/(120*10**3*4*math.pi))

#print(10**14.3)
#print(10**14)
#print(2**47)