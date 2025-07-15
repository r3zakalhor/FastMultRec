#!/bin/sh

Numbersimulation=25
dupcost_values=(3 10 50 100)
losscost=1
threshold=70

for dir_name in sim_2WGD*; do

    echo "$dir_name"

    for (( i=1; i<=$Numbersimulation; i++ )); do
        newname="sim_${i}"
        if [ -s "$dir_name/$newname/s_tree.trees" ]; then

            for t in 90; do
                for d in 1; do
                    gen_file="applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree-b1000_rerooted.txt"

                    if [ -s "$dir_name/$newname/$gen_file" ]; then
                        ./FastMultRec -d 3 -l 1 -gf "$dir_name/$newname/applied_loss_fix_all_genetrees_edited.txt" -sf "$dir_name/$newname/s_tree.newick" -o "$dir_name/$newname/out_simphy.txt" -al simphy &
			./FastMultRec -d 3 -l 1 -gf "$dir_name/$newname/$gen_file" -sf "$dir_name/$newname/s_tree.newick" -o "$dir_name/$newname/out_lca_improvedTreesDL_b1000_unclean.txt" -al lca &
                        ./FastMultRec -d 3 -l 1 -gf "$dir_name/$newname/$gen_file" -sf "$dir_name/$newname/s_tree.newick" -o "$dir_name/$newname/out_greedydown3_improvedTreesDL_b1000_unclean.txt" -al fastgreedy &
                        ./FastMultRec -d 10 -l 1 -gf "$dir_name/$newname/$gen_file" -sf "$dir_name/$newname/s_tree.newick" -o "$dir_name/$newname/out_greedydown10_improvedTreesDL_b1000_unclean.txt" -al fastgreedy &
                        ./FastMultRec -d 50 -l 1 -gf "$dir_name/$newname/$gen_file" -sf "$dir_name/$newname/s_tree.newick" -o "$dir_name/$newname/out_greedydown50_improvedTreesDL_b1000_unclean.txt" -al fastgreedy &
                        ./FastMultRec -d 100 -l 1 -gf "$dir_name/$newname/$gen_file" -sf "$dir_name/$newname/s_tree.newick" -o "$dir_name/$newname/out_greedydown100_improvedTreesDL_b1000_unclean.txt" -al fastgreedy &
                    fi
                done
            done

            wait  # Ensure all parallel jobs finish before continuing

            # Dups in gis
            prefix="out"
            suffix="unclean.txt"
            for file in "$dir_name/$newname/$prefix"*"$suffix"; do
                if [[ -f "$file" ]]; then
                    echo "Processing file: $file"
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
