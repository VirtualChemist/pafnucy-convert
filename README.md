# Helper Scripts

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
