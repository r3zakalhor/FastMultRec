import dendropy
import os
import random
import numpy as np
import argparse

# Parse arguments
parser = argparse.ArgumentParser()

parser.add_argument('-a', type=float, default=1.062409952497)
parser.add_argument('-b', type=float, default=0.133307705766)
parser.add_argument('-c', type=float, default=0.195517800882)
parser.add_argument('-d', type=float, default=0.223514845018)
parser.add_argument('-e', type=float, default=0.294405416545)

parser.add_argument('-theta', type=float, default=0.469075709819)
parser.add_argument('-theta1', type=float, default=0.558949940165)
parser.add_argument('-theta2', type=float, default=0.488093447144)

parser.add_argument('-alpha', help="The shape parameter.", type=float, default=0.370209777709)
parser.add_argument('-n', help="The number of categories to use (n>1).", type=int, default=4)

parser.add_argument('--intp', help="Simulated gene trees.", default='scaled_true_gene_trees.tre')

parser.add_argument('--seed', type=int, help="Random seed for reproducibility.", default=None)

parser.add_argument('--output', help="Output file path to save the sequences.", default=None)

args = parser.parse_args()

# Arguments
intp = args.intp
a = args.a
b = args.b
c = args.c
d = args.d
e = args.e
theta = args.theta
theta1 = args.theta1
theta2 = args.theta2
alpha = args.alpha
n = args.n
seed = args.seed
output_file_path = args.output if args.output else os.path.dirname(intp)

# Set the seed if provided
if seed is not None:
    random.seed(seed)
    print(f"Random seed set to: {seed}")
else:
    print("No seed provided. Using default random behavior.")

# Read the simulated gene trees, handling duplicate taxa labels
try:
    trees = dendropy.TreeList.get(path=intp, schema="newick")
except dendropy.dataio.newickreader.NewickReaderDuplicateTaxonError as e:
    print(f"Error parsing tree: {e}")
    exit(1)

# Add default branch lengths of 1 to any missing branches
for tree in trees:
    for node in tree.postorder_node_iter():
        if node.is_internal() and node.edge_length is None:
            node.edge_length = 1.0  # Default branch length (you can adjust this)

# Frequencies, in order A C G T.
piA = theta1 * (1 - theta)
piC = (1 - theta2) * theta
piG = theta2 * theta
piT = (1 - theta1) * (1 - theta)

# Mutation rates
P = 2 * (a * piC * piT
         + b * piA * piT
         + c * piG * piT
         + d * piA * piC
         + e * piC * piG
         + piA * piG)
AC = d * piC / P
AG = piG / P
AT = b * piT / P
CG = e * piG / P
CT = a * piT / P
GT = c * piT / P

# Output file path
if not os.path.exists(output_file_path):
    os.makedirs(output_file_path)

# Evolve sequence of length 500
for i in range(len(trees)):
    if seed is not None:
        random.seed(seed)

    # Write tree to a temporary file
    trees[i].write(path='tmp_tree.tre', schema='newick')

    # Run seq-gen to generate sequences for each tree
    os.system(f'/usr/bin/seq-gen -mGTR -l500 -a{alpha} -g{n} -f{piA},{piC},{piG},{piT} -r{AC},{AG},{AT},{CG},{CT},{GT} < tmp_tree.tre > {output_file_path}/simulated_sequences_{i}.phy')

    # Check if the sequence file is generated and not empty
    output_sequence_file = f'{output_file_path}/simulated_sequences_{i}.phy'
    if os.path.exists(output_sequence_file) and os.path.getsize(output_sequence_file) > 0:
        with open(output_sequence_file, 'r') as f:
            lines = f.readlines()
            if len(lines) > 1:  # Ensure there's more than 1 line
                sequence = lines[1].strip()  # Assuming sequence is in the second line
                with open(f'{output_file_path}/all_sequences.phy', 'a') as all_seqs_file:
                    all_seqs_file.write(f"{sequence}\n")
            else:
                print(f"Warning: Sequence file {output_sequence_file} is empty or malformed.")
    else:
        print(f"Error: Sequence generation failed for tree {i}. File does not exist or is empty.")

print(f"Sequence generation completed. All sequences are saved in '{output_file_path}/all_sequences.phy'.")
