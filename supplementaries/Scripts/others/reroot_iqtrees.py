import sys
import os
from Bio import Phylo
from io import StringIO

def midpoint_reroot(newick_file):
    # Define output filename
    output_file = newick_file.rsplit(".", 1)[0] + "_rerooted." + newick_file.rsplit(".", 1)[-1]

    with open(newick_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            
            # Read tree
            tree = Phylo.read(StringIO(line), "newick")
            
            # Perform midpoint rerooting
            tree.root_at_midpoint()
            
            # Write rerooted tree to output file
            Phylo.write(tree, outfile, "newick")

    print(f"Rerooted trees saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <newick_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    midpoint_reroot(input_file)
