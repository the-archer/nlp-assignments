import sys
from glob import glob
import string
import math
import pickle
from tokenizer.py import getTokens

def two_class_classify(path):
	para = pickle.load(open("nbmodel.txt", "rb"))
	docs = glob(path+"*/*/*/*.txt")
	f1 = open("nboutput.txt", "w")
	for d in docs:
		c1 = applyMultinomialNB(["deceptive", "truthful"], para[0][0], para[0][1], para[0][2], d)
		c2 = applyMultinomialNB(["positive", "negative"], para[1][0], para[1][1], para[1][2], d)
		f1.write(c1 + " " + c2 + " " + d + '\n')
	f1.close()

	
def applyMultinomialNB(C, V, prior, condprob, d):
	tokens = []
	with open(d, "r") as f1:
		for line in f1:
			tokens += getTokens(line.rstrip('\n'))
	score = dict()
	best = float("-inf")
	maxc = ""
	for c in C:
		score[c] = prior[c]
		for token in tokens:
			if token in V:
				score[c] += condprob[token][c]
		if score[c] > best:
			maxc = c
			best = score[c]
	return maxc

if __name__ == '__main__':
	path = sys.argv[1]
	two_class_classify(path)
