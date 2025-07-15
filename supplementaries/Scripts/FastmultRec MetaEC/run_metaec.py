import os
import subprocess
import csv
import re

# Function to parse a single node and extract species ID and Num Gis
def parse_node_label(node_label):
    # Strip whitespace and split the label into words
    parts = node_label.strip().split()

    # Get the species ID (first word)
    species_id = parts[0]

    # Default Num Gis to 0
    num_gis = 0
    
    # Check if there is an 'epigtcount' field (which is the third word)
    if len(parts) > 2:
        # Look for epigtcount=X
        match = re.search(r'epigtcount=(\d+)', node_label)
        if match:
            num_gis = match.group(1)  # Extract the number after epigtcount=
    
    return species_id, num_gis

# Function to correctly parse the Newick tree
def parse_newick(newick):
    nodes = []
    node = ''
    stack = []
    leaf_flag = False  # Flag to determine if the current node is a leaf

    # Iterate through the tree character by character
    for i, char in enumerate(newick):
        if char == '(':
            # Start of a new internal node (subtree)
            if node:
                nodes.append((node, leaf_flag))
            node = ''
            leaf_flag = True  # Reset flag for internal node
        elif char == ')':
            # End of a subtree
            if node:
                nodes.append((node, leaf_flag))
            node = ''
            leaf_flag = False  # Set flag to True for leaf node after ')'
        elif char == ',':
            # Nodes are separated by commas, save the current node
            if node:
                nodes.append((node, leaf_flag))
            node = ''
            leaf_flag = True  # Internal node flag
        else:
            # Accumulate the node label
            node += char

    # Last node
    if node:
        nodes.append((node, leaf_flag))

    return nodes

# Loop through all directories
for main_dir in os.listdir("."):
    if main_dir.startswith("sim_2WGD_") and os.path.isdir(main_dir):  # Main directory pattern
        for i in range(1, 26):  # Loop through sim_1 to sim_100
            sim_dir = os.path.join(main_dir, f"sim_{i}")
            if os.path.isdir(sim_dir):
                # Path to input files

                # Define input and output file paths for the first script
                genetree_input = os.path.join(sim_dir, "applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree-b1000_rerooted.txt")
                genetree_output = os.path.join(sim_dir, "applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree-b1000_rerooted_metaec.txt")
                subprocess.run(["python", "reformat_Gtrees_metaec.py", genetree_input, genetree_output])


                genetree_input = os.path.join(sim_dir, "applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree-b1000_rerooted_metaec.txt")

                out_file = os.path.join(sim_dir, "out_metaec_uncleaned.txt")
                newick_input = os.path.join(sim_dir, "s_tree.newick")
                newick_output = os.path.join(sim_dir, "s_tree_metaec.newick")
                print(sim_dir)

                # Run the reformat_Strees_metaec.py script if it exists
                try:
                    subprocess.run(["python", "reformat_Strees_metaec.py", newick_input, newick_output], check=True)
                except subprocess.CalledProcessError:
                    print(f"Error running reformat_Strees_metaec.py for {newick_input}")
                    continue  # Skip this simulation and continue

                newick_input = os.path.join(sim_dir, "s_tree_metaec.newick")

                # Run the metaec.py script (assumes this script is available)
                try:
                    subprocess.run(["python", "metaec.py", "--gene_trees", genetree_input, "--species_tree", newick_input, "--out_file", out_file], check=True)
                except subprocess.CalledProcessError:
                    print(f"Error running metaec.py for {sim_dir}")
                    continue  # Skip this simulation and continue

                # Check if MetaEc_out file exists
                if not os.path.isfile(out_file):
                    print(f"MetaEc_out file not found for {sim_dir}, skipping this simulation.")
                    continue  # Skip to next simulation if the output file is missing

                # Read the MetaEc_out file and find the line that starts with outspeciestree_worec=
                try:
                    with open(out_file, "r") as f:
                        lines = f.readlines()
                        for line in lines:
                            if line.startswith('outspeciestree_worec='):
                                newick_line = line
                                match = re.search(r'outspeciestree_worec="(.*)"', newick_line)
                                if match:
                                    newick_tree = match.group(1)

                                    # Parse the Newick tree and extract the required information
                                    species_data = []
                                    
                                    # Parse the tree properly, handling nested structures
                                    nodes = parse_newick(newick_tree)
                                    
                                    for node, is_leaf in nodes:
                                        # Strip whitespace around the node and split it into parts (words)
                                        species_id, num_gis = parse_node_label(node)

                                        # Check if the node is a leaf or internal
                                        if is_leaf:
                                            # Leaf node: Add ' ' around species ID
                                            species_id = f"'{species_id}'"  # Wrap species ID in quotes
                                        else:
                                            # Internal node: No ' ' around species ID
                                            species_id = species_id  # No quotes around species ID

                                        # Append the species ID and Num Gis to the data list
                                        species_data.append([species_id, num_gis])

                                    # Write the extracted data to CSV
                                    csv_output = os.path.join(sim_dir, "MetaEc_out_uncleaned.csv")
                                    with open(csv_output, mode="w", newline="") as csvfile:
                                        csv_writer = csv.writer(csvfile)
                                        csv_writer.writerow(["Species ID", "Num Gis"])  # Header
                                        csv_writer.writerows(species_data)
                                break  # Found the line, no need to continue looping through lines
                except FileNotFoundError:
                    print(f"MetaEc_out file not found for {sim_dir}, skipping.")
                    continue  # Skip to next simulation if the output file is missing
                except Exception as e:
                    print(f"Error reading MetaEc_out for {sim_dir}: {e}")
                    continue  # Continue if any other error occurs
