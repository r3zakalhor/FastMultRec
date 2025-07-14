#!/bin/sh

cd Fungi/reanalyzed


prefix="improvedTreesDL"

#for file in "$prefix"*; do

echo file



		../../segmentalreconcile_MV5_GD -d 5 -l 1 -gf improvedTreesDL_20_1_moreThan16Species.txt -sf speciesTree.newick -o improvedTreesDL_20_1_moreThan16Species_out_lca.txt -spsep '_'  -al lca&
		../../segmentalreconcile_MV5_GD -d 1700 -l 1 -gf improvedTreesDL_20_1_moreThan16Species.txt -sf speciesTree.newick -o improvedTreesDL_20_1_moreThan16Species_out_greedy1700.txt -spsep '_' -al fastgreedy& 

		wait
#done

