#/bin/bash
declare -a arr=("OT2D" "KH" "KH_MHD" "MHDBW2D" "BW2D" "LOOP2D")
declare -a Spc=("O" "p" "He")
declare -a Ks=("10" "50" "100")



## now loop through the above array
for i in "${Spc[@]}"
do
	for j in "${Ks[@]}"
	do
		echo "mv ${i}_sInJ.K$j.0001.h5part ${i}_sInj.K$j.0001.h5part" 
	done
done

