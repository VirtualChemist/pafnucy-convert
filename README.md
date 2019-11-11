# Helper Scripts

## Setting up your environment
The following instructions recount how I've gone about setting up my
environment on the rice machines.

### Installing Python requirements
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

### Installing MGL Tools

Navigate to http://mgltools.scripps.edu/downloads. Copy the link to the proper
Tarball installer. Run the following commands.
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
