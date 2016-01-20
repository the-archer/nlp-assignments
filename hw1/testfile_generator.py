
with open("testfile.txt", "wb") as f1:
	for i in range(0, 65536):
		a  = i//256
		b = i%256
		f1.write(bytes([a, b]))
