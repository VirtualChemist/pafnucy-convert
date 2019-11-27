import csv
import os
import subprocess

PROTEIN_DIR = 'protein_pdbqt'
LIGAND_DIR = 'ligand_pdbqt'
OUTDIR = 'docked'
LOGDIR = 'vina_logs'
CSV_FILE = 'pairs.csv'
CONFIG = 'conf.txt'

if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

vina = "{}/bin/vina".format(os.environ['VINA_ROOT'])

with open(CSV_FILE, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    rows = list(reader)
    progress = 0
    for ligand, protein in rows:
        progress += 1
        print("Docking pair {}/{}: {} to {}".format(progress, len(rows),
                ligand, protein))
        protein_id = protein.strip().replace('/', '.').replace(' ', '.')
        protein_file = "{}/{}.pdbqt".format(PROTEIN_DIR, protein_id)
        ligand_file = "{}/{}.pdbqt".format(LIGAND_DIR, ligand)
        outfile = "{}/{}_{}.pdb".format(OUTDIR, protein_id, ligand)
        logfile = "{}/{}_{}.txt".format(LOGDIR, protein_id, ligand)
        out = subprocess.check_output([vina, '--receptor', protein_file,
                '--ligand', ligand_file, '--config', CONFIG, '--out', outfile],
                stderr=subprocess.STDOUT)
        with open(logfile, 'a', encoding='utf-8') as log:
            log.write(out.decode('utf-8'))
