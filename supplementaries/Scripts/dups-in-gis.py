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

def count_apparent_duplications(species_id, genetrees):
    """ Count apparent duplications for an internal node species_id in the GENETREES section """
    duplication_count = 0
    gene_tree_matches = re.findall(r'<GENETREES>(.*?)</GENETREES>', genetrees, re.DOTALL)
    if not gene_tree_matches:
        return duplication_count

    for gene_tree in gene_tree_matches:
        individual_trees = gene_tree.strip().split(';')
        treeid = 0
        for tree_str in individual_trees:
            treeid += 1
            if tree_str.strip():
                try:
                    tree = Phylo.read(StringIO(tree_str), "newick")
                    for clade in tree.find_clades():
                        if clade.name and (clade.name.startswith(f'{species_id}_Dup') or f'_{species_id}_Dup_' in clade.name):
                            left_set = extract_leaf_names(clade.clades[0])
                            right_set = extract_leaf_names(clade.clades[1])
                            if left_set & right_set:
                                duplication_count += 1
                            break
                except Exception:
                    continue  # Skip trees with format errors
    return duplication_count

def parse_input_file(input_file):
    with open(input_file, 'r') as f:
        content = f.read()

    # Extract species IDs from SPECIESTREE section
    species_tree = re.search(r'<SPECIESTREE>(.*?)</SPECIESTREE>', content, re.DOTALL)
    if species_tree:
        species_tree = species_tree.group(1).strip()
        node_ids = re.findall(r'(\'?\d+\'?)', species_tree)
    else:
        raise ValueError('SPECIESTREE section not found in the input file.')

    # Initialize result: [Species ID, Num Gis, Num App]
    result = [[node_id, 0, 0] for node_id in node_ids]

    # Extract DUPS_PER_SPECIES section
    dups_per_species = re.search(r'<DUPS_PER_SPECIES>(.*?)</DUPS_PER_SPECIES>', content, re.DOTALL)
    species_counts = defaultdict(set)

    if dups_per_species:
        dups_per_species = dups_per_species.group(1).strip()
        species_pattern = re.compile(r'\[(.*?)\]\s+(.*?)\s*(?=\[|$)')
        matches = species_pattern.findall(dups_per_species)

        for species_id_raw, gi_lines in matches:
            species_id = species_id_raw.strip("'")
            gis = re.findall(r'\(G(\d+)\)', gi_lines)
            unique_gis = set(gis)
            species_counts[species_id] = len(unique_gis)

        for entry in result:
            node_id = entry[0].strip("'")
            if node_id in species_counts:
                entry[1] = species_counts[node_id]  # Num Gis
    else:
        raise ValueError('DUPS_PER_SPECIES section not found in the input file.')

    # Extract GENETREES section and compute apparent duplications
    genetrees_section = re.search(r'<GENETREES>(.*?)</GENETREES>', content, re.DOTALL)
    if genetrees_section:
        genetrees = content  # Keep full content in case of multiple GENETREES sections

        for entry in result:
            node_id = entry[0].strip("'")
            if entry[0].startswith("'") and entry[0].endswith("'"):
                entry[2] = entry[1]  # For leaves, use same as Num Gis
            else:
                entry[2] = count_apparent_duplications(node_id, genetrees)  # Internal node
    else:
        raise ValueError('GENETREES section not found in the input file.')

    return result

def save_to_csv(results, input_file):
    csv_file = f"{input_file}.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Species ID', 'Num Gis', 'Num App'])
        writer.writerows(results)
    print(f"Saved results to {csv_file}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python script.py input_file')
        sys.exit(1)
    
    input_file = sys.argv[1]
    try:
        result = parse_input_file(input_file)
        save_to_csv(result, input_file)
    except ValueError as e:
        print(f'Error: {e}')
