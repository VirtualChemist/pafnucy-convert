## PyMol scripting file to run commands
# Usage: 'pymol -c get_blocks.pml'
# Note: Make sure a conda environment running python3 ccd ..is activated, and run this script in the directory containing ligand_out.pdbqt and protein.pdbqt.
# Date last modified: 11/28/19

run ../../pdbqt_to_mol2_ligand_and_pocket.py
get_ligand ./ligand_out.pdbqt
delete all
get_pocket("./protein.pdbqt", "./ligand.mol2")
