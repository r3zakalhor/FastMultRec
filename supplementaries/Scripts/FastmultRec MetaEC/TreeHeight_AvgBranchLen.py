import csv
import sys
from ete3 import Tree

def calculate_tree_metrics(newick_string):
    """Calculates tree height and average branch length for a given Newick string."""
    tree = Tree(newick_string, format=1)  # format=1 to read branch lengths
    
    # Tree height: Maximum root-to-leaf path sum
    tree_height = max(node.get_distance(tree) for node in tree.iter_leaves())

    # Collect all branch lengths except the root branch
    branch_lengths = [node.dist for node in tree.traverse() if not node.is_root()]
    
    # Average branch length (excluding root branch)
    avg_branch_length = sum(branch_lengths) / len(branch_lengths) if branch_lengths else 0

    return tree_height, avg_branch_length

def process_trees_in_file(input_file):
    """Processes a file containing multiple Newick trees (one per line) and saves results to CSV."""
    results = []
    
    with open(input_file, 'r') as f:
        for index, line in enumerate(f, start=1):
            newick_tree = line.strip()
            if newick_tree:  # Skip empty lines
                try:
                    tree_height, avg_branch_length = calculate_tree_metrics(newick_tree)
                    results.append([index, tree_height, avg_branch_length])
                except Exception as e:
                    print(f"Error processing tree on line {index}: {e}")

    # Create output CSV name based on input file name
    output_csv = input_file.rsplit(".", 1)[0] + ".csv"

    # Write results to CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Tree Number", "Tree Height", "Avg Branch Length"])
        writer.writerows(results)

    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    process_trees_in_file(input_file)
