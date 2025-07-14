import os
import glob
import argparse
from ete3 import Tree

def calculate_tree_height(tree):
    # Calculate the longest path from the root to any leaf
    return max(node.get_distance(tree) for node in tree.get_leaves())

def scale_branch_lengths(input_file, givennumber):
    output_file = input_file.replace(
        "applied_loss_fix_all_genetrees_edited.txt", 
        f"applied_loss_fix_all_genetrees_edited_scaledby_{givennumber}_h.txt"
    )
    
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            try:
                tree = Tree(line, format=1)  # Load tree with branch lengths
                
                # Calculate tree height h
                h = calculate_tree_height(tree)
                
                # Scale all branch lengths
                scale_factor = givennumber / h
                for node in tree.traverse():
                    if not node.is_root():
                        node.dist *= scale_factor
                
                # Store root name and branch length
                root_name = tree.name
                root_branch_len = tree.dist

                # Manually construct Newick with root name and branch length included
                if tree.is_root():
                    tree.name = root_name
                    tree.dist = root_branch_len
                    newick = f"{tree.write(format=1)[:-1]}{root_name}:{root_branch_len};"
                else:
                    newick = tree.write(format=1)
                    
                # Write the scaled tree to the output file
                outfile.write(newick + "\n")
                
            except Exception as e:
                print(f"Skipping malformed tree in {input_file}: {line}\nError: {e}")
                continue

    print(f"Processed: {input_file} ? {output_file}")

def process_directories(base_dir, givennumber):
    # Find all matching directories
    for sim_wgd_dir in glob.glob(os.path.join(base_dir, "secu*")):
        for sim_i in range(1, 26):  # Iterate over sim_1 to sim_25
            sim_i_dir = os.path.join(sim_wgd_dir, f"sim_{sim_i}")
            input_file = os.path.join(sim_i_dir, "applied_loss_fix_all_genetrees_edited.txt")

            if os.path.exists(input_file):
                scale_branch_lengths(input_file, givennumber)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scale branch lengths in Newick trees based on tree height")
    parser.add_argument("base_dir", help="Base directory containing sim_1WGD* directories")
    parser.add_argument("givennumber", type=float, help="Scaling number to adjust branch lengths")
    
    args = parser.parse_args()
    process_directories(args.base_dir, args.givennumber)
