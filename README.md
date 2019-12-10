# Pafnucy Data Conversion Scripts

## Setting up your environment
The following instructions recount how I've gone about setting up my
environment on the rice machines.

### Installing Python requirements
I created a Python3 virtual environment, though you could probably skip this
and move right to instaling requirements.
```
virtualenv -p python3 venv
```

Activate the virtual environment by running:
```
source venv/bin/activate
```

Install requirements by running:
```
pip install -r requirements.txt
```

You can deactivate the virtual environment with:
```
deactivate
```

### Installing AutoDock Vina

Navigate to http://vina.scripps.edu/download.html. Copy the link to the Linux
download. Run the following commands.
```
curl -O [link]
tar xzvf autodock_vina_1_1_2_linux_x86.tgz
```

I recommend adding this line to your `.bashrc` file, since the docking script
relies on this variable being set.
```
export VINA_ROOT="[wherever you installed AutoDock Vina]"
```
Example:
```
export VINA_ROOT="$HOME/autodock_vina_1_1_2_linux_x86"
```

### Installing MGL Tools

Navigate to http://mgltools.scripps.edu/downloads. Copy the link to the proper
tarball installer. Run the following commands.
```
curl -O [link]
tar -xzf [filename]
cd [folder name]
./install.sh
```

I recommend adding this line to your `.bashrc` file, since some of these
scripts rely on this variable being set.
```
export MGL_ROOT="[wherever you installed MGL Tools]"
```
Example:
```
export MGL_ROOT="$HOME/mgltools_x86_64Linux2_1.5.6"
```

### Installing PyMol
The version of PyMol pre-installed on the rice machines is old, so you must
install a new version. Navigate to https://pymol.org/2/#download. Copy the link
for the proper install file. Run the following commands.
```
curl -O [link]
tar -jxf [filename]
```

Do NOT add `pymol/bin` to your path. It includes an anaconda installation that
may mess with things. Instead, create a symlink to the PyMol binary somewhere
in your path. For example, I ran
```
cd ~
mkdir bin
cd bin
ln -s ~/pymol/bin/pymol pymol
```
and added this line to my `.bashrc` file:
```
export PATH="$HOME/bin:$PATH"
```

### Cloning Pafnucy
Clone the repository:
```
git clone git@gitlab.com:jspayd/pafnucy.git
```
Add this line to your `.bashrc`:
```
export PAFNUCY_ROOT="[wherever you cloned pafnucy to]"
```
For example:
```
export PAFNUCY_ROOT="$HOME/pafnucy"
```

## Converting ligand SMILES strings into PDB files

Use the `ligand_smiles_to_pdb.py` script for this. It reads from `smiles.csv`
and outputs to the `ligand_pdb` directory.

If you haven't already, activate your virtual environment:
```
source venv/bin/activate
```

Then run the script:
```
python ligand_smiles_to_pdb.py
```

## Getting relative side chain distances from amino acids

Use the `side_chain_dists.py` script for this. It reads from the `aminoacid_pdbs`
directory and outputs to the `aminoacid_dists` directory.

If you haven't already, activate your virtual environment:
```
source venv/bin/activate
```

Then run the script:
```
python side_chain_dists.py
```

## Getting the PDB files of translations from hNaV1.7

Use the `create_protein_translation_pdbs.py` script for this. It reads from the 
`aminoacid_dists` directory and the `base_protein.pdb` and `protein_translations.csv` 
files and outputs to the `protein_pdb` directory.

If you haven't already, get the relative side chain distances:
```
python side_chain_dists.py
```

Then run the script:
```
python create_protein_translation_pdbs.py
```

## Converting ligand PDB files into PDBQT files
Make sure you have your `MGL_ROOT` variable set. Then run:
```
./ligand_pdb_to_pdbqt.sh
```
This takes files from the `ligand_pdb` directory and puts the converted files
in the `ligand_pdbqt` directory.

## Converting protein PDB files into PDBQT files
Make sure you have your `MGL_ROOT` variable set. Then run:
```
./protein_pdb_to_pdbqt.sh
```
This takes files from the `protein_pdb` directory and puts the converted files
in the `protein_pdbqt` directory.

## Docking the ligands to the proteins
Make sure you have your `VINA_ROOT` variable set. Then run:
```
python3 dock.py
```
This takes files from the `protein_pdbqt` and `ligand_pdbqt` directories and
outputs files in the `docked` directory. It uses the configuration file
`conf.txt`. Logs are placed in the `vina_logs` directory.

By default, this command will not dock pairs that have already been docked. To
do so, add the `-o` command line option:
```
python3 dock.py -o
```

## Blocking the docked pairs
Make sure you've installed PyMol and are running version 2.3.4.
```
./prep_pockets.sh
```
This takes files from the `docked` directory, creates a directory for each file
in the `blocked` directory, and creates protein and ligand files in each
created directory.

## Preparing HDF files for running through pafnucy
Make sure you have your `PAFNUCY_ROOT` environment variable set. If using the
GPU environment, use one of the oat machines by running the following command
from one of the rice machines:
```
srun --pty --partition=gpu --gres=gpu:1 --qos=interactive $SHELL -l
```
Then run:
```
./pafnucy_prepare.sh [options]
```
This reads from the `blocked` directory and the `affinities.csv` file and
outputs HDF files in the `datasets` directory for the training, validation, and
test datasets. By default, these files are `data_train.hdf`, `data_val.hdf`,
and `data_test.hdf` respectively, but these can be configured with the options
below.

Options (all are optional)
* `--shuffle`, `-s`: shuffle the dataset before partitioning. The default is to
  not shuffle if this option is not specified.
* `--train`, `-tr`: a number between 0 and 1 representing the fraction of the
  dataset that should be used for training. This is 1 by default.
* `--val`, `-v`: a number between 0 and 1 representing the fraction of the
  dataset that should be used for validation. This is 0 by default.
* `--prefix`, `-p`: the prefix to use for the data files. This is "data" by
  default.

The portion of the dataset that is not partitioned to the training or
validation set will be partitioned to the test set.

Example:
```
./pafnucy_prepare.sh --shuffle --train 0.8 --val 0.1 --prefix data2
```
