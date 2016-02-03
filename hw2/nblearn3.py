import sys
from glob import glob
import string
import math
import pickle
from tokenizer import getTokens


def four_class_classification(path):
	docpath = dict()
	docpath["deceptive_positive"] = glob(path+"positive*/deceptive*/*/*.txt")		
	docpath["truthful_positive"] = glob(path+"positive*/truthful*/*/*.txt")
	docpath["deceptive_negative"] = glob(path+"negative*/deceptive*/*/*.txt")
	docpath["truthful_negative"] = glob(path+"negative*/truthful*/*/*.txt")
	para = []
	para.append(trainMultinomialNB(["deceptive_positive", "truthful_positive", "deceptive_negative", "truthful_negative"], docpath))
	#para.append(trainBernoulliNB(["deceptive_positive", "truthful_positive", "deceptive_negative", "truthful_negative"], docpath))
	#print (para[1])
	pickle.dump(para, open("nbmodel.txt", "wb"))


def two_class_classification(path):
	docpath = dict()
	docpath["deceptive"] = glob(path+"*/deceptive*/*/*.txt")		
	docpath["truthful"] = glob(path+"*/truthful*/*/*.txt")
	docpath["positive"] = glob(path+"positive*/*/*/*.txt")
	docpath["negative"] = glob(path+"negative*/*/*/*.txt")
	para = []
	para.append(trainMultinomialNB(["deceptive", "truthful"], docpath))
	#para.append(trainBernoulliNB(["deceptive", "truthful"], docpath))
	para.append(trainMultinomialNB(["positive", "negative"], docpath))
	#para.append(trainBernoulliNB(["positive", "negative"], docpath))
	#print (para[1])
	pickle.dump(para, open("nbmodel.txt", "wb"))

def SelectFeatures(D, c, k, tokcount, V):
	#V = ExtractVocabulary(D)
	L = []
	for t in V:
		util = ComputeFeatureUtility(D, t, c, tokcount)
		L.append((util, t))
	L.sort(reverse=True)
	return set([L[x][1] for x in range(10, min(len(L), k))])
	

def ComputeFeatureUtility(D, t, c, tokcount):
	return MaxFreqBased(D, t, c, tokcount)


def MaxFreqBased(D, t, c, tokcount):
	if t in tokcount[c]:
		return tokcount[c][t]
	else:
		return 0


def ExtractVocabulary(d):
	V = set()
	for doc in d:
		with open(doc, "r") as f1:
			for line in f1:
				tokens = getTokens(line.rstrip('\n'))
				V = V | set(tokens)
	return V

def trainBernoulliNB(C, D):
	Vocab = set()
	N = 0
	for c in C:
		Vocab |= ExtractVocabulary(D[c])
		N += len(D[c])
	#print (Vocab)
	prior = dict()
	condprob = dict()
	for v in Vocab:
		condprob[v] = dict()
	for c in C:
		Nc = len(D[c])
		prior[c] = (Nc/N)
		#print (prior[c])
		T = dict() 
		for doc in D[c]:
			t = dict()
			with open(doc, "r") as f1:
				for line in f1:
					tokens = getTokens(line.rstrip('\n'))
					for token in tokens:
						t[token] = 1
							
			for token in t:
				if token in T:
					T[token] += 1
				else:
					T[token] = 1
			

		for v in Vocab:
			if v in T:
				condprob[v][c] = (T[v] + 1)/(Nc + 2)
			else:
				condprob[v][c] = 1/(Nc+2)
			
	return [Vocab, prior, condprob]


def trainMultinomialNB(C, D):
	Vocab = set()
	N = 0
	tokcount = dict()
	features = set()
	for c in C:
		Vocab |= ExtractVocabulary(D[c])
		N += len(D[c])
	for c in C:
		tokcount[c] = dict()
		for doc in D[c]:
			with open(doc, "r") as f1:
				for line in f1:
					tokens = getTokens(line.rstrip('\n'))
					for token in tokens:
						if token in tokcount[c]:
							tokcount[c][token] += 1
						else:
							tokcount[c][token] = 1
		features |= SelectFeatures(D, c, 5000, tokcount, Vocab)

	#features = Vocab
	#print (Vocab)
	prior = dict()
	condprob = dict()
	for v in features:
		condprob[v] = dict()
	for c in C:
		Nc = len(D[c])
		prior[c] = math.log(Nc/N)
		#print (prior[c])
		
		
							
				
						
		summ = 0
		for v in features:
			if v not in tokcount[c]:
				tokcount[c][v] = 0
			summ += (tokcount[c][v]+1)
		#print (c)
		#print (summ - len(Vocab))
		#print (len(Vocab))
		for v in features:
			cp = math.log((tokcount[c][v]+1)/summ)
			condprob[v][c] = cp
			
	return [features, prior, condprob]

def main(path):
	two_class_classification(path)
	#four_class_classification(path)


if __name__ == '__main__':
	main(sys.argv[1])
