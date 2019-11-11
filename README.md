# Helper Scripts

## Setting up your environment

### Python requirements
I recommend creating a Python3 virtual environment first.
```
virtualenv -p python3 venv
```

Activate the virtual environment by running:
```
source venv/bin/activate
```

Install dependencies by running:
```
pip install -r requirements.txt
```

You can deactivate the virtual environment with:
```
deactivate
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
