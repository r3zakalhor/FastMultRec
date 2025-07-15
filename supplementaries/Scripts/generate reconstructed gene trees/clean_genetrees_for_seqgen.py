import os
import argparse
from collections import defaultdict
from Bio import Phylo
from io import StringIO

def make_leaf_names_unique(tree):
    """Modify leaf names to ensure uniqueness by changing the last '_0' to '_X'."""
    
    leaf_name_counts = defaultdict(int)

    for clade in tree.get_terminals():
        if clade.name:
            original_name = clade.name

            if original_name in leaf_name_counts:
                # Modify the last number to make it unique
                base_name = "_".join(original_name.split("_")[:-1])  # Keep "A_0"
                new_name = f"{base_name}_{leaf_name_counts[original_name] + 1}"  # Increment last digit
                leaf_name_counts[original_name] += 1
            else:
                new_name = original_name

            leaf_name_counts[new_name] += 1
            clade.name = new_name  # Assign unique name

    return tree

def clean_newick_tree(newick):
    """Clean Newick tree by removing extra parentheses, internal node names, 
       ensuring unique leaf names, and setting root branch length to 0.0001."""
    
    # Parse tree
    tree = Phylo.read(StringIO(newick), "newick")
    
    # Remove internal node names
    for clade in tree.find_clades():
        if not clade.is_terminal():
            clade.name = None  # Remove internal node name

    # Ensure unique leaf names
    tree = make_leaf_names_unique(tree)

    # Set root branch length to 0.0001
    if tree.root.branch_length is not None:
        tree.root.branch_length = 0.0001

    # Convert tree back to string
    output = StringIO()
    Phylo.write(tree, output, "newick")
    return output.getvalue().strip()

def process_file(file_path):
    """Process a given file and save cleaned trees to a new file."""
    
    output_file = file_path.replace(".txt", "_cleaned.txt")

    with open(file_path, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            line = line.strip()
            if line:
                try:
                    cleaned_tree = clean_newick_tree(line)
                    outfile.write(cleaned_tree + "\n")
                except Exception as e:
                    print(f"Skipping tree due to error: {e}")

    print(f"Cleaned trees saved to: {output_file}")

def process_directories(base_dir):
    """Find matching directories and process their files."""
    
    for dir_name in os.listdir(base_dir):
        if dir_name.startswith("secu"):
            sim_1WGD_path = os.path.join(base_dir, dir_name)

            for i in range(1, 26):  # i from 1 to 25
                sim_i_path = os.path.join(sim_1WGD_path, f"sim_{i}")

                if os.path.isdir(sim_i_path):
                    file_path = os.path.join(sim_i_path, "applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h.txt")

                    if os.path.exists(file_path):
                        print(f"Processing: {file_path}")
                        process_file(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Newick trees in specific directories.")
    parser.add_argument("base_dir", help="Path to the base directory containing sim_1WGD directories.")
    args = parser.parse_args()

    process_directories(args.base_dir)
