PROTEIN_IN="protein_pdbqt"
LIGAND_IN="ligand_pdbqt"
DIR_OUT="docked"
DIR_LOG="vina_logs"
DIR_ERR="vina_err"

mkdir -p $DIR_OUT
mkdir -p $DIR_LOG
mkdir -p $DIR_ERR
let NUM_PROTEINS="$(find ${PROTEIN_IN} -maxdepth 1 -type f | wc -l)"
let NUM_LIGANDS="$(find ${LIGAND_IN} -maxdepth 1 -type f | wc -l)"

let protein_count=0

for protein_file in $PROTEIN_IN/*; do
  protein="$(basename -- $protein_file)"
  protein="${protein%.*}"
  let protein_count=$protein_count+1
  echo "Docking ligands to receptor $protein_count/$NUM_PROTEINS: $protein"
  let ligand_count=0
  for ligand_file in $LIGAND_IN/*; do
    ligand="$(basename -- $ligand_file)"
    ligand="${ligand%.*}"
    let ligand_count=$ligand_count+1
    echo "  Docking ligand $ligand_count/$NUM_LIGANDS: $ligand"
    outfile="$DIR_OUT/${protein}_${ligand}.pdb"
    logfile="$DIR_LOG/${protein}_${ligand}.txt"
    errfile="$DIR_ERR/${protein}_${ligand}.txt"
    $VINA_ROOT/bin/vina --receptor "$protein_file" --ligand "$ligand_file" \
      --config conf.txt --out "$outfile" --log "$logfile" \
      >/dev/null 2>"$errfile"
  done
done
