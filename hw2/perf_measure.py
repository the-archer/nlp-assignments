
C = ["deceptive", "truthful", "positive", "negative"]
TP = dict()
FP = dict()
FN = dict()

for c in C:
	TP[c] = 0
	FP[c] = 0
	FN[c] = 0

with open("nboutput.txt", "r") as f1:
	for line in f1:
		sp = line.split()
		if sp[0] in sp[2]:
			TP[sp[0]] += 1
		else:
			FP[sp[0]] += 1
		if sp[1] in sp[2]:
			TP[sp[1]] += 1
		else:
			FP[sp[1]] += 1

FN[C[0]] = FP[C[1]]
FN[C[1]] = FP[C[0]]
FN[C[2]] = FP[C[3]]
FN[C[3]] = FP[C[2]]

precision = dict()
recall = dict()
fscore = dict()
tot = 0
for c in C:
	recall[c] = TP[c]/(TP[c] + FN[c])
	precision[c] = TP[c]/(TP[c] + FP[c])
	fscore[c] = 2*(precision[c]*recall[c])/(precision[c] + recall[c])
	print (c + ": " + "Recall: " + str(recall[c]) + "  " + "Precision: " + str(precision[c]) + '\n')
	tot += fscore[c]
print ("Avg Fscore: " + str(tot/4) + '\n')

