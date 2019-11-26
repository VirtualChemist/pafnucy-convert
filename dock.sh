PROTEIN_IN="ligand_pdbqt"
LIGAND_IN="ligand_pdbqt"
DIR_OUT="docked"
DIR_LOG="vina_logs"
DIR_ERR="vina_err"

CENTER_X=0
CENTER_Y=0
CENTER_Z=0
SIZE_X=1
SIZE_Y=1
SIZE_Z=1

mkdir -p $DIR_OUT
mkdir -p $DIR_LOG
mkdir -p $DIR_ERR
let NUM_PROTEINS="$(find ${PROTEIN_IN} -maxdepth 1 -type f | wc -l)"

let protein_count=0

for protein_file in $PROTEIN_IN/*; do
  protein="$(basename -- $protein_file)"
  protein="${protein%.*}"
  let protein_count=$protein_count+1
  echo "Docking ligands to receptor $protein_count/$NUM_PROTEINS: $protein"
  for ligand_file in $LIGAND_IN/*; do
    ligand="$(basename -- $ligand_file)"
    ligand="${ligand%.*}"
    outfile="$DIR_OUT/${protein}_${ligand}.pdb"
    logfile="$DIR_LOG/${protein}_${ligand}.txt"
    errfile="$DIR_ERR/${protein}_${ligand}.txt"
    $VINA_ROOT/bin/vina --receptor "$protein_file" --ligand "$ligand_file" \
      --center_x $CENTER_X --center_y $CENTER_Y --center_z $CENTER_Z \
      --size_x $SIZE_X --size_y $SIZE_Y --size_z $SIZE_Z \
      --out "$outfile" --log "$logfile" >/dev/null 2>"$errfile"
  done
done
