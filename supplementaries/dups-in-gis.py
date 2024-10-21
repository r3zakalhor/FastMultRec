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
        # Extract all species IDs including those in quotes
        node_ids = re.findall(r'(\'?\d+\'?)', species_tree)
    else:
        raise ValueError('SPECIESTREE section not found in the input file.')

    # Create the 2D array with node IDs and counts
    result = []
    for node_id in node_ids:
        result.append([node_id, 0])


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
                if entry[0] == species_id_raw:
                    entry[1] = len(unique_gis)

        return result
    else:
        raise ValueError('DUPS_PER_SPECIES section not found in the input file.')

def print_results(results):
    for entry in results:
        species_id = entry[0]
        count = entry[1]
        if species_id.isdigit():
            print(f"{species_id} {count}")
        else:
            print(f"{species_id} {count}")

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
        result = parse_input_file(input_file)
        #print_results(result)
        save_to_csv(result, input_file)
    except ValueError as e:
        print(f'Error: {e}')
