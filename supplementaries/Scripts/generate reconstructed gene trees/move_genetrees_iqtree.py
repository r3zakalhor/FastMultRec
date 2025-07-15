import os
import shutil
import argparse
import re

def move_and_rename_files(source_dir):
    # Get all files in the source directory
    for filename in os.listdir(source_dir):
        match = re.match(r"(sim_[^_]+_[^_]+)_sim_(\d+)_genetrees\.txt", filename)
        
        if match:
            first_dir = match.group(1)  # Extract first directory name
            second_dir = f"sim_{match.group(2)}"  # Extract second directory name
            
            # Construct destination path
            dest_dir = os.path.join(first_dir, second_dir)
            
            # Ensure destination directory exists
            #os.makedirs(dest_dir, exist_ok=True)
            
            # Define new filename
            new_filename = "applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree.txt"
            
            # Move and rename the file
            src_path = os.path.join(source_dir, filename)
            dest_path = os.path.join(dest_dir, new_filename)
            shutil.move(src_path, dest_path)
            
            print(f"Moved {filename} to {dest_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move and rename files based on their names.")
    parser.add_argument("source_dir", help="Path to the directory containing the files")
    args = parser.parse_args()
    
    move_and_rename_files(args.source_dir)
