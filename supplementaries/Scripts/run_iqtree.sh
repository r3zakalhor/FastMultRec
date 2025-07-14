#!/bin/bash

# Loop through all directories starting with sim_1WGD*
for dir in secu*; do
    # Check if it's a directory
    [ -d "$dir" ] || continue

    # Loop through sim_x where x is between 1 and 25
    for x in {1..25}; do
        sim_dir="$dir/sim_$x"

        # Check if sim_x exists
        [ -d "$sim_dir" ] || continue

        # Define output file inside sim_x
        OUTPUT_FILE="$sim_dir/applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree-b1000.txt"
        
        # Clear previous output file for this sim_x
        > "$OUTPUT_FILE"

        # Loop through i from 0 to 100
        for i in {0..100}; do
            phy_file="$sim_dir/simulated_sequences_${i}.phy"

            # Check if the input file exists
            if [ -f "$phy_file" ]; then
                echo "Running IQ-TREE on $phy_file"
                iqtree -s "$phy_file" -bb 1000 -nt AUTO -redo

                tree_file="${phy_file}.treefile"

                # Check if tree file was created and add first line to output file
                if [ -f "$tree_file" ]; then
                    head -n 1 "$tree_file" >> "$OUTPUT_FILE"
                else
                    echo "Warning: Tree file not found for $phy_file"
                fi
            fi
        done
    done
done

echo "Processing complete. Output files created inside each sim_x."
