#!/bin/bash

# Define an array of d values
#d_values=("d2" "d3" "d4" "d5" "d10" "d20" "d30" "d50" "d70" "d100")
d_values=("d5")
# Loop through each d value
for d in "${d_values[@]}"; do
    # Run the command with the current d value
    python csv_aggregator_algorithm.py WGD3Simphy_S1_G100_Duprate stats_out_fix_loss_MV2_${d}_l1_t70_GV2_1.csv stats_out_fix_loss_MV1_${d}_l1_t70_GV2_1.csv stats_out_fix_loss_MV2_sto2000tmp1_${d}_l1_t70_GV2_1.csv "Our approach(default)" "Our approach(disable down moves)" "Our approach(stochastic)" 
mv combined_results.pdf greedy_stoc_${d}.pdf

done
