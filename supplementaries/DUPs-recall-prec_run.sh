#!/bin/sh


for dir in "WGD3"*; do
	python DUPs-recall-prec-V2.py "$dir" 80 200

done