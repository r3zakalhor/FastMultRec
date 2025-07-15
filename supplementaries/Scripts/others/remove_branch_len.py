import sys
import os
import re
import glob

def remove_branch_lengths(newick):
    """Removes branch lengths from a Newick tree string."""
    return re.sub(r':\d+(\.\d+)?', '', newick)

def process_newick_file(input_file):
    """Processes a single Newick file to remove branch lengths."""
    output_file = input_file.replace(".txt", "_without_branchlen.txt")

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if line:  # Skip empty lines
                outfile.write(remove_branch_lengths(line) + '\n')

def process_all_files(base_path):
    """Finds and processes all matching files in the given base path."""
    for i in range(1, 26):  # Loop over sim_1 to sim_25
        sim_path = os.path.join(base_path, f"sim_0WGD*/sim_{i}")
        files_to_process = glob.glob(os.path.join(sim_path, "applied_loss_fix_all_genetrees_edited.txt")) + \
                           glob.glob(os.path.join(sim_path, "applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree_rerooted.txt"))

        for file in files_to_process:
            print(f"Processing: {file}")
            process_newick_file(file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <base_path>")
        sys.exit(1)

    base_path = sys.argv[1]
    process_all_files(base_path)
