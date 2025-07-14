#!/bin/sh

Numbersimulation=100
dupcost_values=(2 3 4 5 10 20 30 50 70 100)
losscost=1
threshold=70
#dir_name="WGD2Simphy_S1_G100_Duprate_u-gb_0.1"
#stats_out=$dir_name/stats_out_fix_loss_d100_l1_t70_GV2_1.csv
#gen_file_name="all_genetrees_edited.txt"
#gen_file_name="applied_loss_fix_all_genetrees_edited.txt"
gen_file_name="applied_loss_fix_NNI_K5_all_genetrees_edited.txt"
#gen_file_name="applied_loss_decNum_all_genetrees_edited.txt"


for dir_name in "WGD3"*; do

echo "$dir_name"


for (( i=1; i<=$Numbersimulation; i++ ))
do
	newname="sim_${i}"
	#maxheight=$(head -n 1 "$dir_name/$newname/maxheight.txt")
	maxheight="-"

	if [ -s $dir_name/$newname/s_tree.trees ]; then


		./segmentalreconcile_MV5_GD -d 2 -l 1 -gf $dir_name/$newname/applied_loss_fix_NNI_K1_all_genetrees_edited.txt -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_lca_NNI_K1.txt -al lca&
		./segmentalreconcile_MV5_GD -d 5 -l 1 -gf $dir_name/$newname/applied_loss_fix_NNI_K1_all_genetrees_edited.txt -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_greedydown5_NNI_K1.txt -al fastgreedy&
		./segmentalreconcile_MV5_GD -d 100 -l 1 -gf $dir_name/$newname/applied_loss_fix_NNI_K1_all_genetrees_edited.txt -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_greedydown100_NNI_K1.txt -al fastgreedy&

		./segmentalreconcile_MV5_GD -d 2 -l 1 -gf $dir_name/$newname/applied_loss_fix_NNI_K5_all_genetrees_edited.txt -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_lca_NNI_K5.txt -al lca&
		./segmentalreconcile_MV5_GD -d 5 -l 1 -gf $dir_name/$newname/applied_loss_fix_NNI_K5_all_genetrees_edited.txt -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_greedydown5_NNI_K5.txt -al fastgreedy&
		./segmentalreconcile_MV5_GD -d 100 -l 1 -gf $dir_name/$newname/applied_loss_fix_NNI_K5_all_genetrees_edited.txt -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_greedydown100_NNI_K5.txt -al fastgreedy&

		./segmentalreconcile_MV5_GD -d 2 -l 1 -gf $dir_name/$newname/applied_loss_fix_NNI_K15_all_genetrees_edited.txt -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_lca_NNI_K15.txt -al lca&
		./segmentalreconcile_MV5_GD -d 5 -l 1 -gf $dir_name/$newname/applied_loss_fix_NNI_K15_all_genetrees_edited.txt -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_greedydown5_NNI_K15.txt -al fastgreedy&
		./segmentalreconcile_MV5_GD -d 100 -l 1 -gf $dir_name/$newname/applied_loss_fix_NNI_K15_all_genetrees_edited.txt -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_greedydown100_NNI_K15.txt -al fastgreedy&


		wait


	else
		stats=-1
	fi
done

done