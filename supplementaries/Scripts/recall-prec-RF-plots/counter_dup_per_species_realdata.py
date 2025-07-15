import re
import sys
import csv
from collections import defaultdict

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
            #unique_gis = gis
            species_counts[species_id] = len(unique_gis)
            for entry in result:
                if entry[0] == species_id:
                    entry[1] = len(unique_gis)

        return result, species_tree
    else:
        raise ValueError('DUPS_PER_SPECIES section not found in the input file.')

def modify_and_save_newick(results, species_tree, input_file):
    # Modify the species tree with new labels
    for entry in results:
        old_label = entry[0]
        new_label = f"{entry[0]}_{entry[1]}"
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
        result, species_tree = parse_input_file(input_file)
        # Save results to CSV
        save_to_csv(result, input_file)
        # Modify and save the Newick file
        modify_and_save_newick(result, species_tree, input_file)
    except ValueError as e:
        print(f'Error: {e}')
