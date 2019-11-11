DIR_IN="ligand_pdb"
DIR_OUT="ligand_pdbqt"

mkdir -p $DIR_OUT

for file in ligand_pdb/*; do
  echo "Converting file $file"
  outfile="$(basename -- $file)"
  outfile="$DIR_OUT/${outfile%.*}.pdbqt"
  $MGL_ROOT/bin/python \
    "$MGL_ROOT/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py" \
    -l "$file" -o "$outfile"
done
