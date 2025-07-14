#!/bin/sh


#NOTE: ALL THIS ONLY WORKS IF nb_gene_trees_per_sim IS AT LEAST 100 (because of simphy zero-padding)

nb_simulations=25
nb_gene_trees_per_sim=100
gen_file_name="all_genetrees_edited.txt"

out_dir="WGD1Simphy_S1_G100_Duprate-7"
dup_rate="f:0.0000001"
loss_rate="f:ld"

out_dir=$1
dup_rate=$2
loss_rate="f:ld"

simphy_exe="/data/simphy/SimPhy/bin/simphy"


if [ $# -ne 2 ]; then
    echo "Please specify two arguments: output_directory dup_rate "
    exit 1  # Exit with an error code
fi

rm -r $out_dir
mkdir $out_dir



for (( i=1; i<=$nb_simulations; i++ ))
do
	seed=$RANDOM	#note: seed will be put in sim_${i} directory
	echo seed=$seed
	eval $simphy_exe -sb f:0.000001 -gt f:0.0 -gg f:0.0 -gp f:0.0 -gb u:-25,-15 -ld $dup_rate -lb $loss_rate -lt f:0.0 -lg f:0.0 -rs 1 -rl f:$nb_gene_trees_per_sim -rg 1 -o $out_dir -sp f:2 -su f:0.00001 -sg f:1 -sl U:50,110 -st f:1000000 -om 1 -v 3 -od 1 -op 1 -oc 1 -on 1 -ol 1 -cs $seed
	
	cd $out_dir
	newname="sim_${i}"
	rm -r $newname
	mv 1 $newname
	cd ..

	echo "SimPhy is done"

	echo $seed > $out_dir/$newname/seed.txt

	


	cd $out_dir
	cp ${out_dir}.command $newname/${newname}.command
	cd $newname 
	cat g_trees* >> all_genetrees.txt
	echo "Gene trees are combined into all_genetrees.txt"

	cd ..
	cd ..

	
	
	
	#maxheight=$(head -n 1 "$out_dir/$newname/maxheight.txt")
	maxheight="-"
	
	if [ -s $out_dir/$newname/s_tree.trees ]; then

		python post-order-labeling.py $out_dir/$newname/s_tree.trees $out_dir/$newname/s_tree.newick

		echo "python map_gene_trees_oneWGD.py ${out_dir}/${newname}/all_genetrees.txt ${out_dir}/${newname}/all_genetrees_edited.txt ${out_dir}/${newname}"
		python map_gene_trees.py $out_dir/$newname/all_genetrees.txt $out_dir/$newname/all_genetrees_edited.txt $out_dir/$newname

	fi
	
	echo "Species tree is in s_tree.newick, Gene trees are in all_genetrees_edited.txt"
done


#apply losses

lossrates=("decNum" "decBoth" "fix")

for (( i=1; i<=$nb_simulations; i++ ))
do	
	newname="sim_${i}"
	if [ -s $out_dir/$newname/s_tree.trees ]; then
		for loss in "${lossrates[@]}"; do
			if [ $loss == "fix" ]; then
				out_name="applied_loss_fix_all_genetrees_edited.txt"
				python apply_losses_on_simphy.py $out_dir/$newname/$out_name $out_dir/$newname/all_genetrees_edited.txt 1 0 1 1

			fi
		done

	else

		stats=-1
	
	fi
	echo "$newname done!"
done


