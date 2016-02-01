import string

def getTokens(line):
	words = line.split()
	tokens = []
	for word in words:
		s = word
		for c in string.punctuation:
			s = s.replace(c, "")
		s = s.lower()
		tokens.append(s)
	return tokens