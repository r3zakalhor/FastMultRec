#!/bin/sh


for dir in "WGD1"*; do
	python DUPs-recall-prec-V3-genetrees.py "$dir"

done