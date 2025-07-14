import os
import dendropy

# Fixed Newick tree with all branches having explicit lengths
newick_tree = "(((70_0_0:0.08536,(48_0_0:0.04504,29_0_0:0.04504):0.04031):0.16056,(((26_0_0:0.00936,45_0_0:0.00936):0.00363,40_0_0:0.01298):0.16762,((42_0_0:0.00845,59_0_0:0.00845):0.05496,(34_0_0:0.02196,72_0_0:0.02196):0.04145):0.11719):0.06532):0.36056,((58_0_0:0.27675,((44_0_0:0.26803,46_0_0:0.26803):0.00708,39_0_0:0.27511):0.00164):0.09544,((14_0_0:0.17252,(49_0_0:0.10828,((22_0_0:0.01263,(30_0_0:0.00707,73_0_0:0.00707):0.00556):0.06022,24_0_0:0.07285):0.03543):0.06425):0.15122,((38_0_0:0.07285,30_0_0:0.07285):0.06609,(25_0_0:0.02118,16_0_0:0.02118):0.11776):0.18481):0.04844):0.23429):0.00010;"
# Write the Newick tree to a temporary file
tree_file = "test_tree.tre"
with open(tree_file, "w") as f:
    f.write(newick_tree + "\n")

# Validate the Newick format
try:
    tree = dendropy.Tree.get_from_path(tree_file, schema="newick", suppress_internal_node_taxa=True, suppress_leaf_node_taxa=True)
    print("? Newick tree is valid.")
except Exception as e:
    print(f"? Invalid Newick tree: {e}")
    exit(1)

# Run seq-gen (modify path if needed)
seq_gen_command = f"/usr/bin/seq-gen -mGTR -l500 -a0.5 -g4 -f0.25,0.25,0.25,0.25 < {tree_file}"
print("?? Running seq-gen...")
output = os.popen(seq_gen_command).read()

# Print the generated sequence
print("? Generated Sequence:\n", output if output.strip() else "? Error: No sequence generated.")
