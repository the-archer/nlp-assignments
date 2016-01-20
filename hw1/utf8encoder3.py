import sys


def encode(inp):
	#print(inp)
	val = inp[0]*256 + inp[1]
	if val < 128:
		valb = bin(val)[2:]
		#print (valb)
		padval = valb.zfill(7)
		
		utf8 = "0" + padval
		#print(utf8)
		

	elif val < 2048:

		valb = bin(val)[2:]
		#print(valb)
		padval = valb.zfill(11)
		#print(padval)
		utf8 = "110" + padval[0:5] + "10" + padval[5:11]

	else:
		valb = bin(val)[2:]
		padval = valb.zfill(16)
		utf8 = "1110" + padval[0:4] + "10" + padval[4:10] + "10" + padval[10:16]
	

	
	ulist = [int(utf8[x:(x+8)], 2) for x in range(0, len(utf8), 8)]
	ulist2 = [utf8[x:(x+8)] for x in range(0, len(utf8), 8)]
	
	#print(ulist)
	#print(ulist2)
	return bytes(ulist)




filepath = sys.argv[1]

f2 = open("utf8encoder_out.txt", "wb")

with open(filepath, "rb") as f1:
	
	inp = f1.read(2)
	while inp:
		outp = encode(inp)
		#print(outp)
		f2.write(outp)
		inp = f1.read(2)

f2.close()
