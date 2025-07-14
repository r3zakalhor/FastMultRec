import csv
import argparse
from ete3 import Tree

def compute_normalized_rf_distance(file1, file2, output_csv):
    with open(file1, 'r') as f1, open(file2, 'r') as f2, open(output_csv, 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(["Tree Number", "RF Distance"])

        for index, (line1, line2) in enumerate(zip(f1, f2), start=1):
            tree1 = Tree(line1.strip(), format=1)
            tree2 = Tree(line2.strip(), format=1)
            
            rf_results = tree1.robinson_foulds(tree2)
            rf_distance = rf_results[0]  # Raw RF distance
            max_rf_distance = rf_results[1]  # Maximum possible RF distance
            
            if max_rf_distance > 0:
                normalized_rf_distance = rf_distance / max_rf_distance
            else:
                normalized_rf_distance = 0  # Avoid division by zero
            
            writer.writerow([index, normalized_rf_distance])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute Normalized Robinson-Foulds distance between trees in two files.")
    parser.add_argument("file1", help="Path to the first file containing Newick trees.")
    parser.add_argument("file2", help="Path to the second file containing Newick trees.")
    parser.add_argument("output", help="Path to the output CSV file.")

    args = parser.parse_args()
    compute_normalized_rf_distance(args.file1, args.file2, args.output)
