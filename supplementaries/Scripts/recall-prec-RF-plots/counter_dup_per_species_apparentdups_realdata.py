import re
import sys
import csv
from collections import defaultdict
from Bio import Phylo
from io import StringIO

def extract_leaf_names(clade):
    """Recursively extract leaf names from a clade."""
    if clade.is_terminal():
        return {clade.name.split('_')[0]}  # Consider only the first substring before '_'
    else:
        leaf_names = set()
        for subclade in clade.clades:
            leaf_names.update(extract_leaf_names(subclade))
        return leaf_names

def parse_input_file(input_file):
    with open(input_file, 'r') as f:
        content = f.read()

    # Extract species tree nodes from SPECIESTREE section
    species_tree = re.search(r'<SPECIESTREE>(.*?)</SPECIESTREE>', content, re.DOTALL)
    if species_tree:
        species_tree = species_tree.group(1).strip()
        # Extract all species IDs including those in quotes and strings
        node_ids = re.findall(r'(\'?\d+\'?|\'[a-zA-Z_]+\'|\d+|[a-zA-Z_]+)', species_tree)
    else:
        raise ValueError('SPECIESTREE section not found in the input file.')

    # Create the 2D array with node IDs and counts
    result = []
    for node_id in node_ids:
        result.append([node_id.strip("'"), 0])  # Remove quotes if present

    # Extract species and counts from DUPS_PER_SPECIES section
    dups_per_species = re.search(r'<DUPS_PER_SPECIES>(.*?)</DUPS_PER_SPECIES>', content, re.DOTALL)
    if dups_per_species:
        dups_per_species = dups_per_species.group(1).strip()
        species_counts = defaultdict(set)  # Using a set to store unique (Gi) identifiers
        species_pattern = re.compile(r'\[(.*?)\]\s+(.*?)\s*(?=\[|$)')

        matches = species_pattern.findall(dups_per_species)
        for species_id_raw, gi_lines in matches:
            species_id = species_id_raw.strip("'")  # Remove quotes from species ID
            gis = re.findall(r'\(G(\d+)\)', gi_lines)
            unique_gis = set(gis)
            species_counts[species_id] = len(unique_gis)
            for entry in result:
                if entry[0] == species_id:
                    entry[1] = len(unique_gis)

        return result, species_tree, content
    else:
        raise ValueError('DUPS_PER_SPECIES section not found in the input file.')

def count_apparent_duplications(species_id, genetrees):
    """ Count apparent duplications for an internal node species_id in the GENETREES section """
    duplication_count = 0

    # Find all gene tree sections
    gene_tree_matches = re.findall(r'<GENETREES>(.*?)</GENETREES>', genetrees, re.DOTALL)
    
    # If gene_tree_matches is empty, return duplication_count
    if not gene_tree_matches:
        return duplication_count

    # Iterate over each gene tree section
    for gene_tree in gene_tree_matches:
        individual_trees = gene_tree.strip().split(';')  # Assuming trees are separated by semicolons
        treeid = 0
        trees = []

        for tree_str in individual_trees:
            treeid += 1
            if tree_str.strip():  # Ensure it's not an empty string
                tree = Phylo.read(StringIO(tree_str), "newick")
                # Find the node with species_id_Dup
                for clade in tree.find_clades():
                    if clade.name and (clade.name.startswith(f'{species_id}_Dup') or f'_{species_id}_Dup_' in clade.name):
                        # Get the left and right sets of leaves
                        left_set = extract_leaf_names(clade.clades[0])  # Left subtree
                        right_set = extract_leaf_names(clade.clades[1])  # Right subtree

                        # Check for intersection of left and right leaf sets
                        if left_set & right_set:  # Non-empty intersection
                            duplication_count += 1
                            trees.append(treeid)
                        break
    #print(species_id)
    #print(trees)
    return duplication_count  

def modify_and_save_newick(results, species_tree, input_file, genetrees_content):
    # Modify the species tree with new labels
    for entry in results:
        old_label = entry[0]
        new_label = f"{entry[0]}_{entry[1]}"
        
        # If it's an internal node, calculate apparent duplications
        if old_label.isdigit():  # Internal node (no quotes)
            apparent_duplications = count_apparent_duplications(old_label, genetrees_content)
            new_label += f"_{apparent_duplications}"
        else:
            new_label += f"_{entry[1]}"
        species_tree = re.sub(rf'\b{re.escape(old_label)}\b', new_label, species_tree)
    
    # Save the modified species tree to a .newick file
    newick_file = f"{input_file}.newick"
    with open(newick_file, 'w') as f:
        f.write(species_tree)
    print(f"Saved modified species tree to {newick_file}")

def save_to_csv(results, input_file):
    csv_file = f"{input_file}.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Species ID', 'Num Gis'])
        writer.writerows(results)
    print(f"Saved results to {csv_file}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python script.py input_file')
        sys.exit(1)
    
    input_file = sys.argv[1]
    try:
        result, species_tree, genetrees_content = parse_input_file(input_file)
        # Save results to CSV
        #save_to_csv(result, input_file)
        # Modify and save the Newick file
        modify_and_save_newick(result, species_tree, input_file, genetrees_content)
    except ValueError as e:
        print(f'Error: {e}')  
