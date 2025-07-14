#!/bin/sh

cd Phylome


prefix="improvedTreesDL"

for file in "$prefix"*; do

echo file



		../segmentalreconcile_MV5_GD -d 5 -l 1 -gf improvedTreesDL_0.9_5.txt -sf species_tree.newick -o "improvedTreesDL_0.9_5_out_lca.txt" -spsep '_'  -al lca&
		../segmentalreconcile_MV5_GD -d 5000 -l 1 -gf improvedTreesDL_0.9_5.txt -sf species_tree.newick -o "improvedTreesDL_0.9_5_out_greedy5000.txt" -spsep '_' -al fastgreedy& 

		wait
done

