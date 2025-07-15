#!/bin/sh


#NOTE: ALL THIS ONLY WORKS IF nb_gene_trees_per_sim IS AT LEAST 100 (because of simphy zero-padding)

nb_simulations=25
nb_gene_trees_per_sim=100
gen_file_name="all_genetrees_edited.txt"

#out_dir="WGD1Simphy_S1_G100_Duprate-7"
#dup_rate="f:0.0000001"
#loss_rate="f:ld"

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
	command="$simphy_exe -rs 1 -rl f:1 -rg 1 -sb ln:-14,1 -sl u:30,80 -st u:100000,10000000 -si u:1,6 -so ln:0,0.1 -gb u:-25,-15 -gt f:gb -ld \"$dup_rate\" -lb \"$loss_rate\" -lt f:0 -lk 1 -sp ln:12,0.5 -sg f:1 -hs ln:1.5,1 -hl ln:1.2,1 -hg ln:1.4,1 -su e:10000000 -o $out_dir/SP_Tree_generate -om 1 -v 1 -od 1 -oc 1 -op 1 -ol 1 -cs $seed"
	echo $command	
	eval $command
	
	cp $out_dir/SP_Tree_generate/1/s_tree.trees  $out_dir/s_tree.trees 

	python simphy_wgd.py -spfile=$out_dir/s_tree.trees -auxfile=$out_dir/myaux.txt -sout=$out_dir/s_tree_modded.trees
	python simphy_wgd.py -spfile=$out_dir/s_tree_modded.trees -auxfile=$out_dir/myaux2.txt -sout=$out_dir/s_tree_modded2.trees
	
	s_tree_modded=$(cat $out_dir/s_tree_modded2.trees)
	
	eval $simphy_exe -sb f:0.000001 -gt f:0.0 -gg f:0.0 -gp f:0.0 -gb u:-25,-15 -ld $dup_rate -lb $loss_rate -lt f:0.0 -lg f:0.0 -rs 1 -rl f:$nb_gene_trees_per_sim -rg 1 -o $out_dir -sp f:2 -su f:0.00001 -sg f:1 -sl U:50,110 -st f:1000000 -om 1 -v 3 -od 1 -op 1 -oc 1 -on 1 -ol 1 -cs $seed -S \'$s_tree_modded\'
	
	cd $out_dir
	newname="sim_${i}"
	rm -r $newname
	mv 1 $newname
	cd ..

	echo $seed > $out_dir/$newname/seed.txt


	for (( j=1; j<=$nb_gene_trees_per_sim; j++ ))
	do
    		ii=$(printf "%03d" $j)
		filename="${ii}.mapsl"
		filename2="${ii}l1g.maplg"
		filename3="g_trees${ii}.trees"
		echo $filename
		python simphy_wgd.py -mode=remap -auxfile=$out_dir/myaux2.txt -slfile=$out_dir/$newname/$filename -lgfile=$out_dir/$newname/$filename2 -genetreefile=$out_dir/$newname/$filename3 > out.txt
	done
	
	for (( j=1; j<=$nb_gene_trees_per_sim; j++ ))
	do
    		ii=$(printf "%03d" $j)
		filename="${ii}.mapsl.modded"
		filename2="${ii}l1g.maplg.modded"
		filename3="g_trees${ii}.trees.modded"
		echo $filename
		python simphy_wgd.py -mode=remap -auxfile=$out_dir/myaux.txt -slfile=$out_dir/$newname/$filename -lgfile=$out_dir/$newname/$filename2 -genetreefile=$out_dir/$newname/$filename3 > out.txt
	done


	cd $out_dir
	cp ${out_dir}.command $newname/${newname}.command
	cd $newname 
	cat g_trees*.modded.modded >> all_genetrees.txt
	echo "gene trees are combined!"

	cd ..
	cd ..
	cp $out_dir/myaux.txt $out_dir/$newname/myaux.txt
	cp $out_dir/myaux2.txt $out_dir/$newname/myaux2.txt
	cp $out_dir/s_tree.trees $out_dir/$newname/source_s_tree.trees
	cp $out_dir/s_tree_modded.trees $out_dir/$newname/s_tree_modded.trees
	cp $out_dir/s_tree_modded2.trees $out_dir/$newname/s_tree_modded2.trees

	
	#maxheight=$(head -n 1 "$out_dir/$newname/maxheight.txt")
	maxheight="-"
	
	if [ -s $out_dir/$newname/s_tree.trees ]; then

		python post-order-labeling.py $out_dir/$newname/source_s_tree.trees $out_dir/$newname/s_tree.newick
		python map_gene_trees_twoWGD.py $out_dir/$newname/all_genetrees.txt $out_dir/$newname/all_genetrees_edited.txt $out_dir/$newname
	fi

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