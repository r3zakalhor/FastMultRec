#!/bin/sh


for dir_name in "sim_1WGD_D"*; do
    #python DUPs-recall-prec-V2-WGD_with_ecceTERA.py "$dir_name" 50 200
    #python DUPs-recall-prec-V2-WGD_with_ecceTERA.py "$dir_name" 80 200

    python DUPs-recall-prec-V2-WGD_with_ecceTERA_metaec.py "$dir_name" 50 200
    python DUPs-recall-prec-V2-WGD_with_ecceTERA_metaec.py "$dir_name" 80 200

    #python DUPs-recall-prec-V2-WGD.py "$dir_name" 80 200
    #python DUPs-recall-prec-V2-SD.py "$dir_name" 20 80


done