import os
import shutil
import glob

def copy_files(source_root, destination_root, filename):
    # Ensure destination root exists
    os.makedirs(destination_root, exist_ok=True)
    
    # Find all matching files
    pattern = os.path.join(source_root, "sim_*", "sim_*", filename)
    files = glob.glob(pattern)
    
    for file_path in files:
        parts = file_path.split(os.sep)
        if len(parts) < 3:
            continue  # Skip unexpected paths
        
        sim_Y = os.path.join(parts[-3], parts[-2])  # Extract sim_Y from path
        dest_dir = os.path.join(destination_root, sim_Y)
        os.makedirs(dest_dir, exist_ok=True)
        
        dest_path = os.path.join(dest_dir, filename)
        shutil.copy2(file_path, dest_path)
        print(f"Copied {file_path} -> {dest_path}")

# Example usage
source_directory = ""
destination_directory = "only_trees"

filenames_to_copy = [ "applied_loss_fix_all_genetrees_edited.txt", "all_genetrees_edited.txt" ]

for file_name in filenames_to_copy:
    copy_files(source_directory, destination_directory, file_name)
