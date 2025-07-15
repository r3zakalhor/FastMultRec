for dir in sim_2WGD_D*; do
    for i in {1..25}; do
        if [ -d "${dir}/sim_${i}" ]; then
            echo "${dir}/sim_${i}"
            python clean_species_tree.py "${dir}/sim_${i}/s_tree.newick" "${dir}/sim_${i}/s_tree_cleaned.newick"

            #for t in 50 60 70 80 90 95 99; do  # Change to "50 60 70 80 90" if using bootstrap values
                #for d in 1 2 3 4 5; do
            for t in 50 70 90 95; do  # Change to "50 60 70 80 90" if using bootstrap values
                for d in 1 5; do
                    ./ecceTERA_linux64 species.file="${dir}/sim_${i}/s_tree_cleaned.newick" \
                        gene.file="${dir}/sim_${i}/applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree-b1000.txt" \
                        dated=0 compute.T=false collapse.threshold=${t} collapse.mode=1 \
                        dupli.cost=${d} loss.cost=1 print.newick=true resolve.trees=1\
                        print.newick.gene.tree.file="${dir}/sim_${i}/applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree_rerooted_improvedTreesDL_ultrafastb1000_${t}_${d}.txt"
                done
            done
        fi
    done
done
