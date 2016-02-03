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

def SelectFeatures(D, c, k, tokcount, V, tokind, C):
	#V = ExtractVocabulary(D)
	L = []
	for t in V:
		util = ComputeFeatureUtility(D, t, c, tokcount, tokind, C)
		L.append((util, t))
	L.sort(reverse=True)
	#print (L[:20])
	return set([L[x][1] for x in range(0, min(len(L), k))])
	

def ComputeFeatureUtility(D, t, c, tokcount, tokind, C):
	#return MaxFreqBased(t, c, tokcount)
	return MutualInfo(D, t, c, tokind, C)

def MutualInfo(D, t, c, tokind, C):
	if t in tokind[c]:
		n11 = tokind[c][t]
	else:
		n11 = 0
	n01 = len(D[c]) - n11
	n10 = 0
	n = 0
	for cl in C:
		if cl != c:
			if t in tokind[cl]:
				n10 += tokind[cl][t]
		n += len(D[c])
	n00 = n - n11 - n01 - n10
	mi = 0
	a = (n11/n)
	if a != 0:
		mi += (n11/n)*math.log((n*n11)/((n10+n11)*(n01+n11)))
	a = (n01/n)
	if a != 0:
		mi += (n01/n)*math.log((n*n01)/((n00+n01)*(n01+n11)))
	
	a = (n10/n)
	if a != 0:
		mi += (n10/n)*math.log((n*n10)/((n10+n11)*(n00+n10)))
	a = (n00/n)
	if a != 0:
		mi += (n00/n)*math.log((n*n00)/((n00+n01)*(n00+n10)))
		
		
	return mi

def MaxFreqBased(t, c, tokcount):
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
	tokind = dict()
	features = set()
	for c in C:
		Vocab |= ExtractVocabulary(D[c])
		N += len(D[c])
	for c in C:
		tokcount[c] = dict()
		tokind[c] = dict()
		for doc in D[c]:
			t = dict()
			with open(doc, "r") as f1:
				for line in f1:
					tokens = getTokens(line.rstrip('\n'))
					for token in tokens:
						if token in tokcount[c]:
							tokcount[c][token] += 1
						else:
							tokcount[c][token] = 1
						t[token] = 1
			for token in t:
				if token in tokind[c]:
					tokind[c][token] += 1
				else:
					tokind[c][token] = 1

	for c in C:
		features |= SelectFeatures(D, c, 2000, tokcount, Vocab, tokind, C)

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
