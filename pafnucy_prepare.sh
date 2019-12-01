olddir=$(pwd)
cd $PAFNUCY_ROOT
conda env create -f environment_cpu.yml
source activate pafnucy_env

TRAINFILE="${olddir}/our_train.hdf"
TESTFILE="${olddir}/our_test.hdf"
VALFILE="${olddir}/our_val.hdf"

# Stolen from https://stackoverflow.com/a/5533586
shuffle() {
   local i tmp size max rand

   # $RANDOM % (i+1) is biased because of the limited range of $RANDOM
   # Compensate by using a range which is a multiple of the array size.
   size=${#array[*]}
   max=$(( 32768 / size * size ))

   for ((i=size-1; i>0; i--)); do
      while (( (rand=$RANDOM) >= max )); do :; done
      rand=$(( rand % (i+1) ))
      tmp=${array[i]} array[i]=${array[rand]} array[rand]=$tmp
   done
}

array=($olddir/blocked/*)

shuffle

let train_len=$(echo "scale=0; ${#array[*]}*0.80/1" | bc)
let test_len=$(echo "scale=0; ${#array[*]}*0.10/1" | bc)
let val_len=${#array[*]}-${train_len}-${test_len}

train_pockets=()
train_ligands=()
test_pockets=()
test_ligands=()
val_pockets=()
val_ligands=()

let cutoff=train_len+test_len

size=${#array[*]}
for ((i=size-1; i>0; i--)); do
    id="$(basename -- ${array[i]})"
    id="${id%.*}"
    cp "${array[i]}/pocket.mol2" "${array[i]}/pocket_$id.mol2"
    cp "${array[i]}/ligand.mol2" "${array[i]}/ligand_$id.mol2"
    if [ $i -lt $train_len ]; then
        train_pockets+=("${array[i]}/pocket_$id.mol2")
        train_ligands+=("${array[i]}/ligand_$id.mol2")
    elif [ $i -lt $cutoff ]; then
        test_pockets+=("${array[i]}/pocket_$id.mol2")
        test_ligands+=("${array[i]}/ligand_$id.mol2")
    else
        val_pockets+=("${array[i]}/pocket_$id.mol2")
        val_ligands+=("${array[i]}/ligand_$id.mol2")
    fi
done

echo "Preparing training data (${#train_pockets[*]} pairs)"
python3 prepare.py -l ${train_ligands[@]} -p ${train_pockets[@]} -o \
    "$TRAINFILE" --affinities "$olddir/affinities.csv"
echo ""
echo "Preparing test data (${#test_pockets[*]} pairs)"
python3 prepare.py -l ${test_ligands[@]} -p ${test_pockets[@]} -o "$TESTFILE" \
    --affinities "$olddir/affinities.csv"
echo ""
echo "Preparing validation data (${#val_pockets[*]} pairs)"
python3 prepare.py -l ${val_ligands[@]} -p ${val_pockets[@]} -o "$VALFILE" \
    --affinities "$olddir/affinities.csv"

echo "Cleaning up temp files"
for ((i=size-1; i>0; i--)); do
    id="$(basename -- ${array[i]})"
    id="${id%.*}"
    rm "${array[i]}/pocket_$id.mol2"
    rm "${array[i]}/ligand_$id.mol2"
done
