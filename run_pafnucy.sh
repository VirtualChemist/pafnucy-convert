cd $PAFNUCY_ROOT
conda env create -f environment_gpu.yml
source activate pafnucy_env

for file in $BLOCKED_ROOT/*/ 
do
	echo "Predicting datapoint $file"
	python3 prepare.py -l ${file}ligand.mol2 -p ${file}pocket.mol2 -o ${file}complexes.hdf
	python3 predict.py -i ${file}complexes.hdf -o ${file}predictions.csv 
done