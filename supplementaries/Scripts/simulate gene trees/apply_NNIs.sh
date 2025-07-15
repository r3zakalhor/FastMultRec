#!/bin/sh

Numbersimulation=100

for dir_name in "WGD3"*; do

for (( i=1; i<=$Numbersimulation; i++ ))
do	
	echo "$dir_name"
	newname="sim_${i}"

	python apply-NNIs.py $dir_name/$newname/applied_loss_fix_all_genetrees_edited.txt 15 $dir_name/$newname/applied_loss_fix_NNI_K15_all_genetrees_edited.txt

	echo "$newname done!"
done

done

