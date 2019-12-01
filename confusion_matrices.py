import os
import math
import baseline
import plot_confusion_matrix
import numpy as np
import matplotlib.pyplot as plt

vinafolder = 'vina_logs/'
blockedfolder = 'blocked/'
metric = None

false_pos = 0
true_neg = 0
false_neg = 0
true_pos = 0

y_true = []
y_pred = []
class_names = ['Won\'t Bind', 'Will Bind']
title = None
matrixfilename = None


while(True):
	print('Which error metrics do you want?')
	print('V for vina, P for original pafnucy, N for n-gram baseline')
	command = input()
	if len(command) > 1 or command not in 'VPN':
		print()
		print('Please input one of [V, P, N]')
		print()
		continue 
	metric = command
	break


with open('affinities_binary.csv', 'r') as examples:
	for j, example in enumerate(examples):
		if j == 0: continue
		row = example.split(',')
		protein_ligand = row[0].replace('ligand_', '')
		klass = int(row[1])

		if metric == 'V':
			title = 'Vina Confusion Matrix'
			matrixfilename = 'vina_matrix.pdf'
			with open(vinafolder + protein_ligand + '.txt', 'r') as f:
				start = None
				for i, line in enumerate(f):
					vina_line = line.split()
					if len(vina_line) == 0: continue
					if vina_line[0] == 'mode':
						start = i
					if start != None:
						if i - start == 3:
							affinity = float(vina_line[1])
							DeltaG = 1000 * affinity
							Ki = math.exp(DeltaG/(1.986 * 298)) * (10 ** 9)
							IC50 = Ki * 2
							if klass == 0:
								y_true.append('Won\'t Bind')
								if IC50 >= 500:
									#classification = 0 
									true_neg += 1
									y_pred.append('Won\'t Bind')
								else:
									#classification = 1
									false_pos += 1
									y_pred.append('Will Bind')
							else: 
								y_true.append('Will Bind')
								if IC50 >= 500:
									#classification = 0 
									false_neg += 1
									y_pred.append('Won\'t Bind')
								else:
									#classification = 1
									true_pos += 1
									y_pred.append('Will Bind')
							break
		elif metric == 'P':
			title = 'Original Pafnucy Confusion Matrix'
			matrixfilename = 'pafnucy_matrix.pdf'
			with open(blockedfolder +  protein_ligand + '.pdb/predictions.csv', 'r') as f:
				for i, line in enumerate(f):
					if i == 0: continue
					pafnucy_line = line.split(',')
					pKi = float(pafnucy_line[1])
					IC50 = (10 ** (-pKi)) * (10 ** 9) * 2
					if klass == 0:
						y_true.append('Won\'t Bind')
						if IC50 >= 500:
							#classification = 0 
							true_neg += 1
							y_pred.append('Won\'t Bind')
						else:
							#classification = 1
							false_pos += 1
							y_pred.append('Will Bind')
					else: 
						y_true.append('Will Bind')
						if IC50 >= 500:
							#classification = 0 
							false_neg += 1
							y_pred.append('Won\'t Bind')
						else:
							#classification = 1
							true_pos += 1
							y_pred.append('Will Bind')
		else:
			baseline.main()
			exit()

print('False Positive:', false_pos)
print('True Negative:', true_neg)
print('False Negative:', false_neg)
print('True Positive:', true_pos)
np.set_printoptions(precision=2)
plot_confusion_matrix.plot_confusion_matrix(np.array(y_true), np.array(y_pred), classes=np.array(class_names),
                      title=title)
plt.savefig(matrixfilename, format='pdf')



