import os
import random
import shutil

nb_simulations = 100
nb_gene_trees = 100
out_dir = "WGD1Simphy_S1_G100_Duprate-7" #was dir_name
gene_tree_filename = "all_genetrees_edited.txt"    #was gen_file_name

dup_rate = "0.0000001"
loss_rate = "f:ld"

#gen_file_name="applied_loss_fix_all_genetrees_edited.txt"
#gen_file_name="applied_loss_decBoth_all_genetrees_edited.txt"
#gen_file_name="applied_loss_decNum_all_genetrees_edited.txt"


if not os.path.exists(out_dir):
    os.makedirs(out_dir)



for i in range(1, nb_simulations + 1)

    seed = random.randint(1, 2**64)

    tmp_dir = os.path.join(out_dir, "SP_Tree_temp")
    sptree_filename = os.path.join(out_dir, "s_tree.trees")
    sptree_wgd_filename = os.path.join(out_dir, "s_tree_wgd.trees")

    #semi-empty simphy run just to generate a species tree in a temp directory
	command_tmp = "./simphy -rs 1 -rl f:1 -rg 1 -sb ln:-14,1 -sl u:30,80 -st u:100000,10000000 -si u:1,6 -so ln:0,0.1 -gb u:-25,-15 -gt f:gb"
    command_tmp += " -ld " + dup_rate + " -lb " + loss_rate + " -lt ln:gt,0.4 -lk 1 -sp ln:12,0.5 -sg f:1 -hs ln:1.5,1 -hl ln:1.2,1 -hg ln:1.4,1 -su e:10000000" + 
    command_tmp += " -o " + tmp_dir 
    command_tmp += " -om 1 -v 1 -od 1 -oc 1 -op 1 -ol 1 -cs " + str(seed)
    
    os.system(command_tmp)
    
    
    #cp $dir_name/SP_Tree_generate/1/s_tree.trees  $dir_name/s_tree.trees 
    shutil.copy(os.path.join(tmp_dir, "1", "s_tree.trees"), sptree_filename)
    
	#apply wgds on this species tree
	#python simphy_wgd.py -spfile=$dir_name/s_tree.trees -auxfile=$dir_name/myaux.txt -sout=$dir_name/s_tree_modded.trees
    command_wgd = "python simphy_wgd.py -spfile=" + sptree_filename + " -auxfile=" + os.path.join(dir_name, "myaux.txt")
    command_wgd += " -sout=" + sptree_wgd_filename
    
    os.system(command_wgd)


    #pass that wgd species tree to simphy and do a real run
    #s_tree_modded=$(cat $dir_name/s_tree_modded.trees)
    with open(sptree_wgd_filename, "r") as file:
        sptree_wgd_newick = file.read()

	command_sim = "./simphy -sb f:0.000001 -gt f:0.0 -gg f:0.0 -gp f:0.0 -ld " + dup_rate + " -lb " + loss_rate + " -lt f:0.0 -lg f:0.0 -rs 1 -rl f:100 -rg 1 -o " + out_dir + " -sp f:2 -su f:0.00001 -sg f:1 -sl U:50,110 -st f:1000000 -om 1 -v 3 -od 1 -op 1 -oc 1 -on 1 -ol 1 -cs " + str(seed) + " -S \"" + sptree_wgd_newick + "\""
	
    os.system(command_sim)


    #simphy creates a directory "/1/" with all stuff in it.  Just rename it to sim_i
    #cd $dir_name
	#newname="sim_${i}"
	#rm -r $newname
	#mv 1 $newname
	#cd ..
    newdirname = os.path.join(out_dir, "sim_" + str(i))
    if not os.path.exists(newdirname):
        shutil.rmtree(newdirname)
    
    shutil.move(os.path.join(out_dir, "1"), newdirname)
    
	

	for j in range(1, 101): #(( j=1; j<=99; j++ ))
        ii = f"{j:02}"
        
        slmap = ii + ".mapsl"
    	lgmap = ii + "l1g.maplg"
        gtrees = "g_trees" + ii + ".trees"
        
        command_remap = "python simphy_wgd.py -mode=remap -auxfile=" + os.path.join(dir_name, "myaux.txt") + " -slfile=" + os.path.join(newdirname, slmap) + " -lgfile=" + os.path.join(newdirname, lgmap) + " -genetreefile=" + os.path.join(newdirname, gtrees) + " > out.txt"
        
        os.system(command_remap)
        
        #ii=$(printf "%02d" $j)
		#filename="${ii}.mapsl"
		#filename2="${ii}l1g.maplg"
		#filename3="g_trees${ii}.trees"
		#echo $filename
		#python simphy_wgd.py -mode=remap -auxfile=$dir_name/myaux.txt -slfile=$dir_name/$newname/$filename -lgfile=$dir_name/$newname/$filename2 -genetreefile=$dir_name/$newname/$filename3 > out.txt
	
	


	cd $dir_name
	cp ${dir_name}.command $newname/${newname}.command
	cd $newname 
	cat g_trees*.modded >> all_genetrees.txt
	echo "gene trees are combined!"

	cd ..
	cd ..
	cp $dir_name/myaux.txt $dir_name/$newname/myaux.txt
	cp $dir_name/s_tree.trees $dir_name/$newname/source_s_tree.trees
	cp $dir_name/s_tree_modded.trees $dir_name/$newname/s_tree_modded.trees

	
	#maxheight=$(head -n 1 "$dir_name/$newname/maxheight.txt")
	maxheight="-"
	
	if [ -s $dir_name/$newname/s_tree.trees ]; then

		python post-order-labeling.py $dir_name/$newname/source_s_tree.trees $dir_name/$newname/s_tree.newick

		python map_gene_trees_oneWGD.py $dir_name/$newname/all_genetrees.txt $dir_name/$newname/all_genetrees_edited.txt $dir_name/$newname

	fi
done


#apply losses

lossrates=("decNum" "decBoth" "fix")

for (( i=1; i<=$Numbersimulation; i++ ))
do	
	newname="sim_${i}"
	if [ -s $dir_name/$newname/s_tree.trees ]; then
		for loss in "${lossrates[@]}"; do
			if [ $loss == "decNum" ]; then
				out_name="applied_loss_decNum_all_genetrees_edited.txt"
				python apply_losses_on_simphy.py $dir_name/$newname/$out_name $dir_name/$newname/all_genetrees_edited.txt 1 0 0 1
			elif [ $loss == "decBoth" ]; then
				out_name="applied_loss_decBoth_all_genetrees_edited.txt"
				python apply_losses_on_simphy.py $dir_name/$newname/$out_name $dir_name/$newname/all_genetrees_edited.txt 1 1 0 0
			elif [ $loss == "fix" ]; then
				out_name="applied_loss_fix_all_genetrees_edited.txt"
				python apply_losses_on_simphy.py $dir_name/$newname/$out_name $dir_name/$newname/all_genetrees_edited.txt 1 0 1 1

			fi
		done

	else

		stats=-1
	
	fi
	echo "$newname done!"
done


