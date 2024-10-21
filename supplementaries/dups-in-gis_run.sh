#!/bin/sh

Numbersimulation=100

for dir in "WGD3"*; do

for (( i=1; i<=$Numbersimulation; i++ ))
do

	newname="sim_${i}"	

	prefix="out_"
	suffix=".txt"
        #suffix=".txt"
	for file in "$dir/$newname/$prefix"*"$suffix"; do
		if [[ -f "$file" ]]; then
        		echo "Found file: $file"
			python dups-in-gis.py "$file"
		fi
	done		

done
done


