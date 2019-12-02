import numpy as np 
import pandas as pd 
import math
import tfbio.net
import matplotlib as mpl
mpl.use('agg')
import seaborn as sns 
sns.set_style('white')
sns.set_context('paper')
sns.set_color_codes()


ids = []
affinity = []
pred = []
rmse = 0
count = 0


with open('affinities.csv', 'r') as datapoints:
	for j, datapoint in enumerate(datapoints):
		if j == 0: continue
		row = datapoint.split(',')
		pdbid = row[0].replace('ligand_', '')
		affin = float(row[1])
		with open('blocked/' + pdbid + '.pdb/predictions.csv') as f:
			for i, line in enumerate(f):
				if i == 0: continue
				pafnucy_line = line.split(',')
				pred_val = float(pafnucy_line[1])
			ids.append(pdbid)
			affinity.append(affin)
			pred.append(pred_val)
			rmse += (pred_val - affin) ** 2
			count += 1
	rmse = math.sqrt(rmse / count)


predictions = pd.DataFrame(data={'pdbid': np.array(ids),
                                 'real': np.array(affinity),
                                 'predicted': np.array(pred)})

grid = sns.jointplot('real', 'predicted', data=predictions, color='green',
                     space=0.0, xlim=(0, 16), ylim=(0, 16),
                     annot_kws={'title': '(rmse=%.3f)' % rmse})


image = tfbio.net.custom_summary_image(grid.fig)
grid.fig.savefig('our_graph_ogp.pdf')
print("RMSE: {}".format(rmse))


