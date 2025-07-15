#!/bin/sh

Numbersimulation=100

dupcost_values=(2 3 4 5 10 20 30 50 70 100)  # Add the desired dupcost values here

for dir in "WGD1"*; do
python dups-in-gis_sum.py $dir out_simphy.txt.csv
python dups-in-gis_sum.py $dir out_lca.txt.csv

for dupcost in "${dupcost_values[@]}"
do
	greedy="out_greedy${dupcost}.txt.csv"
	greedydown="out_greedydown${dupcost}.txt.csv"
	sto="out_stochastic${dupcost}.txt.csv"
	python dups-in-gis_sum.py $dir $greedy
	python dups-in-gis_sum.py $dir $greedydown
	python dups-in-gis_sum.py $dir $sto


done
done


