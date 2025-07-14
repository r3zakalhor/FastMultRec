import argparse
from ete3 import Tree
import random
import os, sys

def clean_single_child_nodes(tree):
    """
    Remove nodes with only one child by connecting the child directly to the parent.
    """
    for node in tree.traverse():
        while len(node.children) == 1:
            child = node.children[0]
            parent = node.up
            if parent:
                parent.remove_child(node)
                parent.add_child(child)
            node = child

def nearest_neighbor_interchange(tree, node):
    """
    Perform NNI at the specified node in a binary tree.
    
    :param tree: A binary Newick tree (ete3.Tree)
    :param node: The node where NNI should be performed.
    """
    parent = node.up
    if parent is None:
        raise ValueError(f"Node {node.name} is the root node, cannot perform NNI.")

    grandparent = parent.up
    if grandparent is None:
        raise ValueError(f"Node {node.name}'s parent is the root node, cannot perform NNI.")
    
    # Identify the other child of the grandparent
    other_child = [child for child in grandparent.children if child != parent][0]
    
    # Detach the subtrees to be swapped
    node_subtree = node.detach()
    other_subtree = other_child.detach()
    
    # Create a new internal node
    new_node = Tree(name="1000_1000_NNI")
    new_node.add_child(node_subtree)
    new_node.add_child(other_subtree)
    
    # Attach the new internal node to the grandparent
    grandparent.add_child(new_node)
    
    # Clean up the tree by removing nodes with only one child
    clean_single_child_nodes(tree)

def perform_k_nnis(tree, k):
    """
    Perform k successive NNIs on random nodes in the tree.
    
    :param tree: A binary Newick tree (ete3.Tree)
    :param k: Number of NNIs to perform.
    """
    nodes = [node for node in tree.traverse() if node.up and node.up.up]  # Exclude root and its children
    if not nodes:
        print("No eligible nodes found for NNI.")
        return

    for _ in range(k):
        node = random.choice(nodes)
        nearest_neighbor_interchange(tree, node)
        # Update the list of eligible nodes after each NNI
        nodes = [node for node in tree.traverse() if node.up and node.up.up]
        if not nodes:
            break

def main():
    parser = argparse.ArgumentParser(description="Perform k NNIs on a Newick tree.")
    parser.add_argument("newick_file", type=str, help="Path to the Newick file containing multiple trees.")
    parser.add_argument("k", type=int, help="Number of NNIs to perform.")
    parser.add_argument("output_file", type=str, help="Path to save the modified Newick file.")
    args = parser.parse_args()
    
    with open(args.newick_file, "r") as f:
        newick_str = f.read().strip()
    
    # Split the file into individual tree strings
    tree_strings = newick_str.split(';')
    tree_strings = [tree_str + ';' for tree_str in tree_strings if tree_str]
    
    modified_trees = []
    for tree_str in tree_strings:
        tree = Tree(tree_str, format=1)

        perform_k_nnis(tree, args.k)

        # Get the Newick string of the modified tree and add it to the list
        newick_string = tree.write(format=1, format_root_node=lambda node: f"[&name={node.name}]")
        modified_trees.append(newick_string)
    
    # Write all modified trees to the output file
    with open(args.output_file, "w") as f:
        f.write('\n'.join(modified_trees))
    
    print("Modified trees saved to:", args.output_file)

if __name__ == "__main__":
    main()
