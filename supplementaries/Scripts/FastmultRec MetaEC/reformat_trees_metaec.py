import os
import subprocess

# Define the main directory pattern
main_dir_pattern = "WGD"

# Loop through all WGD directories
for main_dir in os.listdir("."):
    if main_dir.startswith(main_dir_pattern) and os.path.isdir(main_dir):
        # Loop through sim_1 to sim_100
        for i in range(1, 101):
            sim_dir = os.path.join(main_dir, f"sim_{i}")
            if os.path.isdir(sim_dir):
                # Define input and output file paths for the first script
                genetree_input = os.path.join(sim_dir, "applied_loss_fix_all_genetrees_edited.txt")
                genetree_output = os.path.join(sim_dir, "applied_loss_fix_all_genetrees_edited_cleaned_metaec.txt")
                
                # Define input and output file paths for the second script
                newick_input = os.path.join(sim_dir, "s_tree.newick")
                newick_output = os.path.join(sim_dir, "s_tree_metaec.newick")
                print(sim_dir)
                # Run the first command
                #subprocess.run(["python", "reformat_Gtrees_metaec.py", genetree_input, genetree_output])
                
                # Run the second command
                subprocess.run(["python", "reformat_Strees_metaec.py", newick_input, newick_output])
