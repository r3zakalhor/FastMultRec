#!/bin/sh

Numbersimulation=100
dir_name="sim_0WGD_LN0.3"

lossrates=("decNum" "decBoth" "fix")

for (( i=1; i<=$Numbersimulation; i++ ))
do	
	newname="sim_${i}"
	if [ -s $dir_name/$newname/s_tree.trees ]; then
		for loss in "${lossrates[@]}"; do
			if [ $loss == "fix" ]; then
				out_name="applied_loss_fix_all_genetrees_edited.txt"
				python apply_losses_on_simphy.py $dir_name/$newname/$out_name $dir_name/$newname/all_genetrees_edited.txt 1 0 1 1

			fi
		done

	else

		stats=-1
	
	fi
	echo "$newname done!"
done



