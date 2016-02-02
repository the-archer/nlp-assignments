import sys
import nblearn3
import nbclassify3
import perf_measure


fscores = []

for i in range(1, 5):
	s = "1234"
	p = s.replace(str(i), "")
	nblearn3.main("op_spam_train_"+p+"/")
	nbclassify3.main("op_spam_valid_" + str(i) + "/")
	fscores.append(perf_measure.getMeasure())

print ("Cross-Validation Result: " + str(sum(fscores)/len(fscores)))


