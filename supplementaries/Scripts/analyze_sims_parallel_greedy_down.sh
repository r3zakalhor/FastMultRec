#!/bin/sh

Numbersimulation=25
dupcost_values=(3 10 50 100)
losscost=1
threshold=70

gen_file_name1="applied_loss_fix_all_genetrees_edited.txt"
gen_file_name2="applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree_rerooted_without_branchlen.txt"


for dir_name in "sim_2WGD"*; do

echo "$dir_name"


for (( i=1; i<=$Numbersimulation; i++ ))
do
	newname="sim_${i}"
	if [ -s $dir_name/$newname/s_tree.trees ]; then

		#./FastMultRec -d 2 -l 1 -gf $dir_name/$newname/$gen_file_name1 -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_simphy.txt -al simphy&
		./FastMultRec -d 2 -l 1 -gf $dir_name/$newname/$gen_file_name1 -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_true_lca.txt -al lca&
                ./FastMultRec -d 3 -l 1 -gf $dir_name/$newname/$gen_file_name1 -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_true_greedydown3.txt -al fastgreedy&
		./FastMultRec -d 10 -l 1 -gf $dir_name/$newname/$gen_file_name1 -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_true_greedydown10.txt -al fastgreedy&
                ./FastMultRec -d 50 -l 1 -gf $dir_name/$newname/$gen_file_name1 -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_true_greedydown50.txt -al fastgreedy&
                ./FastMultRec -d 100 -l 1 -gf $dir_name/$newname/$gen_file_name1 -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_true_greedydown100.txt -al fastgreedy&

		./FastMultRec -d 60 -l 1 -gf $dir_name/$newname/$gen_file_name1 -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_true_greedydown60.txt -al fastgreedy&
                ./FastMultRec -d 70 -l 1 -gf $dir_name/$newname/$gen_file_name1 -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_true_greedydown70.txt -al fastgreedy&
                ./FastMultRec -d 80 -l 1 -gf $dir_name/$newname/$gen_file_name1 -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_true_greedydown80.txt -al fastgreedy&
                ./FastMultRec -d 90 -l 1 -gf $dir_name/$newname/$gen_file_name1 -sf $dir_name/$newname/s_tree.newick -o $dir_name/$newname/out_true_greedydown90.txt -al fastgreedy&


		wait
	
	# Dups in gis
	prefix="out_true"
        suffix=".txt"
	for file in "$dir_name/$newname/$prefix"*"$suffix"; do
		if [[ -f "$file" ]]; then
        		echo "Found file: $file"
			python dups-in-gis.py "$file"
		fi
	done		




	else
		stats=-1
	fi
done

    #python DUPs-recall-prec-V2-WGD.py "$dir_name" 80 200
    #python DUPs-recall-prec-V2-SD.py "$dir_name" 20 80

done
