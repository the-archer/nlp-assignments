import codecs

f1 = open("testfile.txt", "rb")
f2 = open("testoutput.txt", "wb")

a = f1.read(2)

while a:
	try:
		b = codecs.decode(a, "utf-16be")
		c = codecs.encode(b, "utf-8")

		f2.write(c)
	except:
		pass
	a = f1.read(2)

f1.close()
f2.close()