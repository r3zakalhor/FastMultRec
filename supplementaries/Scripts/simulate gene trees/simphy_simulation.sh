#!/bin/sh


nb_simulations=100
nb_gene_trees_per_sim=100
gen_file_name="all_genetrees_edited.txt"

#out_dir="WGD0Simphy_S1_G100_Duprate-7"
#dup_rate="f:0.0000001"
loss_rate="f:ld"

out_dir=$1
dup_rate=$2
loss_rate="f:ld"

simphy_exe="~/git/SimPhy/bin/simphy.exe"


mkdir $out_dir



for (( i=1; i<=$nb_simulations; i++ ))
do

	seed=$RANDOM	#note: seed will be put in sim_${i} directory
	echo seed=$seed
	command="$simphy_exe -sb f:0.000001 -gt f:0.0 -gg f:0.0 -gp f:0.0 -gb u:-25,-15 -ld $dup_rate -lb $loss_rate -lt f:0.0 -lg f:0.0 -rs 1 -rl f:$nb_gene_trees_per_sim -rg 1 -o $out_dir -sp f:2 -su f:0.00001 -sg f:1 -sl U:50,110 -st f:1000000 -om 1 -v 3 -od 1 -op 1 -oc 1 -on 1 -ol 1 -cs $seed"
	
	echo $command	
	eval $command
	
	cd $out_dir
	newname="sim_${i}"
	rm -r $newname
	mv 1 $newname
	cp ${out_dir}.command $newname/${newname}.command
	
	echo "$PWD"
	
	cd $newname 
	
	echo "$PWD"
	
	cat g_trees* >> all_genetrees.txt
	echo "gene trees are combined!"
	#bash ../../counter_dup_per_species.sh
	cd ..
	cd ..
	
	if [ -s $out_dir/$newname/s_tree.trees ]; then
		
		commandpo="python post-order-labeling.py $out_dir/$newname/s_tree.trees $out_dir/$newname/s_tree.newick"
		
		echo $commandpo
		eval $commandpo
		#python post-order-labeling.py $out_dir/$newname/source_s_tree.trees $out_dir/$newname/s_tree.newick

		python map_gene_trees.py $out_dir/$newname/all_genetrees.txt $out_dir/$newname/all_genetrees_edited.txt $out_dir/$newname

	fi
done


#apply losses

lossrates=("decNum" "decBoth" "fix")

for (( i=1; i<=$nb_simulations; i++ ))
do	
	newname="sim_${i}"
	if [ -s $out_dir/$newname/s_tree.trees ]; then
		echo "TRUE: -s $out_dir/$newname/s_tree.trees"
		for loss in "${lossrates[@]}"; do
			if [ $loss == "decNum" ]; then
				out_name="applied_loss_decNum_all_genetrees_edited.txt"
				cmdloss="python apply_losses_on_simphy.py $out_dir/$newname/$out_name $out_dir/$newname/all_genetrees_edited.txt 1 0 0 1"
				echo $cmdloss 
				eval $cmdloss
			elif [ $loss == "decBoth" ]; then
				out_name="applied_loss_decBoth_all_genetrees_edited.txt"
				cmdloss="python apply_losses_on_simphy.py $out_dir/$newname/$out_name $out_dir/$newname/all_genetrees_edited.txt 1 1 0 0"
				echo $cmdloss 
				eval $cmdloss
			elif [ $loss == "fix" ]; then
				out_name="applied_loss_fix_all_genetrees_edited.txt"
				cmdloss="python apply_losses_on_simphy.py $out_dir/$newname/$out_name $out_dir/$newname/all_genetrees_edited.txt 1 0 1 1"
				echo $cmdloss 
				eval $cmdloss

			fi
		done

	else
		echo "FALSE: -s $out_dir/$newname/s_tree.trees"
		stats=-1
	
	fi
	echo "$newname done!"
done


