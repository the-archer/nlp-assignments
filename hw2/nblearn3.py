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
	#para.append(trainMultinomialNB(["positive", "negative"], docpath))
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
	para.append(trainMultinomialNB(["positive", "negative"], docpath))
	#print (para[1])
	pickle.dump(para, open("nbmodel.txt", "wb"))






def ExtractVocabulary(d):
	V = set()
	for doc in d:
		with open(doc, "r") as f1:
			for line in f1:
				tokens = getTokens(line.rstrip('\n'))
				V = V | set(tokens)
	return V


def trainMultinomialNB(C, D):
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
		prior[c] = math.log(Nc/N)
		#print (prior[c])
		T = dict() 
		for doc in D[c]:
			with open(doc, "r") as f1:
				for line in f1:
					tokens = getTokens(line.rstrip('\n'))
					for token in tokens:
						if token in T:
							T[token] += 1
						else:
							T[token] = 1
							
				
						
		summ = 0
		for v in Vocab:
			if v not in T:
				T[v] = 0
			summ += (T[v]+1)
		for v in Vocab:
			cp = math.log((T[v]+1)/summ)
			condprob[v][c] = cp
			
	return [Vocab, prior, condprob]

def main(path):
	two_class_classification(path)
	#four_class_classification(path)


if __name__ == '__main__':
	main(sys.argv[1])
