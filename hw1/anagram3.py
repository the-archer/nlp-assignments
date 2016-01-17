import sys

def getPermutations(s):
	if len(s) <= 1:
		return [s]
	perm = getPermutations(s[1:])
	newperm = []
	for w in perm:
		for i in range(0, len(w)+1):
			newperm.append(w[:i]+s[0]+w[i:])
	return newperm






word = sys.argv[1].lstrip('\'').rstrip('\'')
perm = getPermutations(word)
perm.sort()

with open("anagram_out.txt", "w") as f1:
	for w in perm:
		f1.write(w+'\n')

