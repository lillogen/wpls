data = open("Dateien/guess_bin_2.txt","r")
binstring = data.read()
nachricht = ""
for i in range(0, len(binstring), 24):
	seq = binstring[i:i+24]
	seq = seq.replace(',',"")
	seq = seq.replace(' ',"")
	if seq != "\n":
		print(seq)
		charakter = (int(seq,2))
		nachricht+=chr(charakter)
		print(hex(charakter))

print(nachricht)
data.close()