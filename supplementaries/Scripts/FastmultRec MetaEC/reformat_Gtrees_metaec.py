from ete3 import Tree
import sys

def clean_newick(file_path, output_path):
    with open(file_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            
            try:
                tree = Tree(line, format=1)  # Read Newick, ignoring branch lengths
                
                # Remove internal node names and branch lengths
                for node in tree.traverse():
                    node.name = "" if not node.is_leaf() else node.name.split('_')[0]
                    node.dist = 0  # Remove branch lengths
                
                newick_str = tree.write(format=5)
                newick_str = newick_str.replace(':0', '')  # Remove remaining branch length markers
                newick_str = newick_str.replace(';', '')
                outfile.write(newick_str + "\n")  # Write the cleaned tree
            except Exception as e:
                print(f"Skipping malformed tree: {line}")
                print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_newick.py input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    clean_newick(input_file, output_file)
