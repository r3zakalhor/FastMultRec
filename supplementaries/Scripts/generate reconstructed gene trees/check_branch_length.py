import csv
import re
import argparse
from ete3 import Tree

def extract_gene_trees(file1):
    """Extract Newick trees from within <GENETREES> </GENETREES> tags."""
    with open(file1, 'r') as f:
        content = f.read()
    
    match = re.search(r'<GENETREES>(.*?)</GENETREES>', content, re.DOTALL)
    if not match:
        raise ValueError("No <GENETREES> </GENETREES> block found in the file.")
    
    trees = match.group(1).strip().split('\n')
    return [tree.strip() for tree in trees if tree.strip()]

def parse_trees(file1, file2, output_csv, summary_csv):
    """Process gene trees and extract required information."""
    gene_trees = extract_gene_trees(file1)
    with open(file2, 'r') as f:
        reference_trees = [line.strip() for line in f.readlines() if line.strip()]
    
    if len(gene_trees) != len(reference_trees):
        raise ValueError("Mismatch in the number of trees between the two files.")
    
    results = []
    summary_results = []
    
    for i, (gene_tree, ref_tree) in enumerate(zip(gene_trees, reference_trees), start=1):
        gt = Tree(gene_tree, format=1)
        rt = Tree(ref_tree, format=1)
        
        branch_lengths = [node.dist for node in rt.traverse() if node.is_leaf()]
        avg_branch_length = sum(branch_lengths) / len(branch_lengths) if branch_lengths else "NA"
        
        spec_branch_lengths = []
        dup_branch_lengths = []
        num_leaves = 0
        num_spec = 0
        num_dup = 0
        
        for leaf in gt:
            num_leaves += 1
            parent = leaf.up
            if not parent:
                continue
            
            label_parts = parent.name.split('_')
            if len(label_parts) < 2:
                continue
            
            spec_dup_label = label_parts[1]  # Second part of parent label
            ref_leaf = rt.search_nodes(name=leaf.name)
            branch_len = ref_leaf[0].dist if ref_leaf else "NA"
            
            if spec_dup_label == "Spec":
                spec_branch_lengths.append(branch_len)
                num_spec += 1
            elif spec_dup_label == "Dup":
                dup_branch_lengths.append(branch_len)
                num_dup += 1
                
            results.append([i, leaf.name, spec_dup_label, branch_len, avg_branch_length])
        
        avg_spec_branch_length = sum(spec_branch_lengths) / len(spec_branch_lengths) if spec_branch_lengths else "NA"
        avg_dup_branch_length = sum(dup_branch_lengths) / len(dup_branch_lengths) if dup_branch_lengths else "NA"
        
        summary_results.append([i, avg_branch_length, avg_spec_branch_length, avg_dup_branch_length, num_leaves, num_spec, num_dup])
    
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Tree_Index", "Leaf_Name", "Parent_Label", "Branch_Length", "Avg_Branch_Length", "Avg_Spec_Branch_Length", "Avg_Dup_Branch_Length"])
        writer.writerows(results)
    
    with open(summary_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Tree_Index", "Avg_Branch_Length", "Avg_Spec_Branch_Length", "Avg_Dup_Branch_Length", "Num_Leaves", "Num_Spec", "Num_Dup"])
        writer.writerows(summary_results)
    
    print(f"Detailed results saved to {output_csv}")
    print(f"Summary results saved to {summary_csv}")

def main():
    parser = argparse.ArgumentParser(description="Process Newick trees and extract leaf information.")
    parser.add_argument("file1", help="First input file containing Newick trees inside <GENETREES> tags.")
    parser.add_argument("file2", help="Second input file containing reference Newick trees.")
    parser.add_argument("output_csv", help="Output CSV file to store detailed results.")
    parser.add_argument("summary_csv", help="Output CSV file to store summary results.")
    
    args = parser.parse_args()
    parse_trees(args.file1, args.file2, args.output_csv, args.summary_csv)

if __name__ == "__main__":
    main()