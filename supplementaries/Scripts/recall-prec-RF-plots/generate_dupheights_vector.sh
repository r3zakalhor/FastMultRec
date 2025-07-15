#!/bin/sh

Numbersimulation=100
dupcost=2 
losscost=1
threshold=70
dir_name="WGD1Simphy_S1_G100_Duprate_u-gb_1"

#gen_file_name="all_genetrees_edited.txt"
gen_file_name="applied_loss_fix_all_genetrees_edited.txt"
#gen_file_name="applied_loss_decBoth_all_genetrees_edited.txt"
#gen_file_name="applied_loss_decNum_all_genetrees_edited.txt"


for (( i=1; i<=$Numbersimulation; i++ ))
do
	newname="sim_${i}"
	
	if [ -s $dir_name/$newname/s_tree.trees ]; then

		./segmentalreconcile_MV3 -d 2 -l 1 -gf $dir_name/$newname/$gen_file_name -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_simphy_dupheights.txt -al simphy
		
	else
		stats=-1
	fi
done
