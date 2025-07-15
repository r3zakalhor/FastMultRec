#!/bin/bash

for simdir in sim*; do
  if [ -d "$simdir" ]; then
    for subdir in "$simdir"/sim_*; do
      if [ -d "$subdir" ]; then
        filename=$(find "$subdir" -maxdepth 1 -type f -name "applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree_rerooted_improvedTreesDL_ultrafastb1000_90_1.txt")
        if [ -f "$filename" ]; then
          subname=$(basename "$subdir")   # sim_1, sim_2, etc.
          cp "$filename" "$simdir/$subname.txt"
        fi
      fi
    done
  fi
done
