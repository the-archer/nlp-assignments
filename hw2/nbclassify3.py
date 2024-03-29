import sys
from glob import glob
import string
import math
import pickle
from tokenizer import getTokens

def two_class_classify(path):
	para = pickle.load(open("nbmodel.txt", "rb"))
	docs = glob(path+"*/*/*/*.txt")
	f1 = open("nboutput.txt", "w")
	for d in docs:
		c1 = applyMultinomialNB(["deceptive", "truthful"], para[0][0], para[0][1], para[0][2], d)
		c2 = applyMultinomialNB(["positive", "negative"], para[1][0], para[1][1], para[1][2], d)
		#c1 = applyBernoulliNB(["deceptive", "truthful"], para[0][0], para[0][1], para[0][2], d)
		#c2 = applyBernoulliNB(["positive", "negative"], para[1][0], para[1][1], para[1][2], d)
		f1.write(c1 + " " + c2 + " " + d + '\n')
	f1.close()

def four_class_classify(path):
	para = pickle.load(open("nbmodel.txt", "rb"))
	docs = glob(path+"*/*/*/*.txt")
	f1 = open("nboutput.txt", "w")
	for d in docs:
		c = applyMultinomialNB(["deceptive_positive", "truthful_positive", "deceptive_negative", "truthful_negative"], para[0][0], para[0][1], para[0][2], d)
		#c = applyBernoulliNB(["deceptive_positive", "truthful_positive", "deceptive_negative", "truthful_negative"], para[0][0], para[0][1], para[0][2], d)
		c1 = c.split("_")[0]
		c2 = c.split("_")[1]
		f1.write(c1 + " " + c2 + " " + d + '\n')
	f1.close()

def applyBernoulliNB(C, V, prior, condprob, d):
	tokens = set()
	with open(d, "r") as f1:
		for line in f1:
			tokens |= set(getTokens(line.rstrip('\n')))
	score = dict()
	best = float("-inf")
	maxc = ""
	for c in C:
		score[c] = math.log(prior[c])	
		for token in V:
			if token in tokens:
				score[c] += math.log(condprob[token][c])
			else:
				score[c] += math.log(1 - condprob[token][c])
			
		if score[c] > best:
			maxc = c
			best = score[c]
	return maxc


	
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

def main(path):
	two_class_classify(path)
	#four_class_classify(path)


if __name__ == '__main__':
	main(sys.argv[1])
