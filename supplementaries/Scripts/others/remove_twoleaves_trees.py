import os
import sys
from Bio import Phylo
from io import StringIO

def clean_newick_file(file_path):
    cleaned_lines = []
    
    with open(file_path, "r") as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            
            try:
                tree = Phylo.read(StringIO(line), "newick")
                num_leaves = len(tree.get_terminals())

                if num_leaves > 2:
                    cleaned_lines.append(line)  # Keep the tree if it has more than 2 leaves
            except Exception as e:
                print(f"Warning: Skipping invalid line in {file_path}: {line}")

    # Overwrite the original file with cleaned content
    with open(file_path, "w") as outfile:
        outfile.write("\n".join(cleaned_lines) + "\n")

def process_directory(base_dir):
    if not os.path.isdir(base_dir):
        print(f"Error: '{base_dir}' is not a valid directory.")
        sys.exit(1)

    for sim_0WGD_dir in sorted(os.listdir(base_dir)):
        sim_0WGD_path = os.path.join(base_dir, sim_0WGD_dir)
        
        if os.path.isdir(sim_0WGD_path) and sim_0WGD_dir.startswith("sim_0WGD"):
            for i in range(1, 26):  # sim_1 to sim_25
                sim_i_path = os.path.join(sim_0WGD_path, f"sim_{i}")
                
                if os.path.isdir(sim_i_path):
                    file_path = os.path.join(sim_i_path, "applied_loss_fix_all_genetrees_edited.txt")
                    
                    if os.path.exists(file_path):
                        print(f"Processing: {file_path}")
                        clean_newick_file(file_path)
                    else:
                        print(f"File not found: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <base_directory>")
        sys.exit(1)

    base_directory = sys.argv[1]
    process_directory(base_directory)
