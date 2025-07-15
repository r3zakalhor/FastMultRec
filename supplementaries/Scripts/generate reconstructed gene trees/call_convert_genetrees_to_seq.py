import os
import subprocess
import argparse

def process_directories(base_dir):
    """Find matching directories and call the sequence simulation script for each cleaned file."""
    
    for dir_name in os.listdir(base_dir):
        if dir_name.startswith("secu"):
            sim_1WGD_path = os.path.join(base_dir, dir_name)

            for i in range(1, 26):  # i from 1 to 25
                sim_i_path = os.path.join(sim_1WGD_path, f"sim_{i}")

                if os.path.isdir(sim_i_path):
                    file_path = os.path.join(sim_i_path, "applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned.txt")

                    if os.path.exists(file_path):
                        print(f"Processing: {file_path}")
                        
                        # Run your sequence simulation script
                        subprocess.run([
                            "python", "convert_genetrees_to_seq.py", 
                            "--intp", file_path,
                            "--output", sim_i_path
                        ], check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run sequence simulation for cleaned Newick trees.")
    parser.add_argument("base_dir", help="Path to the base directory containing sim_1WGD directories.")
    args = parser.parse_args()

    process_directories(args.base_dir)
