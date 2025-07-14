#!/bin/bash

# Define the root directory and output directory
root_dir="sim_0WGD_D7"
output_dir="${root_dir}_info"

# Create the output directory
mkdir -p "$output_dir"

# List of subdirectories to process: sim_0WGD_D18 and sim_1 to sim_25 inside it
dirs=("$root_dir")
for i in $(seq 1 25); do
    dirs+=("$root_dir/sim_$i")
done

# Loop through each directory and copy matching files into corresponding subdir in output
for dir in "${dirs[@]}"; do
    if [ -d "$dir" ]; then
        # Extract directory name (e.g., sim_1)
        subdir_name=$(basename "$dir")
        target_subdir="$output_dir/$subdir_name"

        # Create subdirectory inside output directory
        mkdir -p "$target_subdir"
        echo "Created $target_subdir"

        # Copy relevant files
        for file in "$dir"/simulated_sequences_*.phy \
                    "$dir"/applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned.txt \
                    "$dir"/applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree_rerooted.txt; do
            if [ -f "$file" ]; then
                echo "Copying $file to $target_subdir"
                cp "$file" "$target_subdir"
            fi
        done
    else
        echo "Directory $dir not found, skipping."
    fi
done
