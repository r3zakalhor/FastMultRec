import os
import sys
import subprocess

# Path to the midpoint rerooting script
REROOT_SCRIPT = "reroot_iqtrees.py"  # Update if the script has a different name or path

def find_and_reroot(base_dir):
    if not os.path.isdir(base_dir):
        print(f"Error: '{base_dir}' is not a valid directory.")
        sys.exit(1)

    for sim_0WGD_dir in sorted(os.listdir(base_dir)):
        sim_0WGD_path = os.path.join(base_dir, sim_0WGD_dir)
        
        # Check if the directory starts with sim_0WGD
        if os.path.isdir(sim_0WGD_path) and sim_0WGD_dir.startswith("sim_1WGD_d7"):
            for i in range(1, 26):  # sim_1 to sim_25
                sim_i_path = os.path.join(sim_0WGD_path, f"sim_{i}")
                
                if os.path.isdir(sim_i_path):
                    # Define the input file path
                    input_file = os.path.join(sim_i_path, "applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned.txt")
                    
                    if os.path.exists(input_file):
                        # Remove lines that start with "File"
                        with open(input_file, "r") as infile:
                            lines = infile.readlines()
                        
                        cleaned_lines = [line for line in lines if not line.startswith("File")]
                        
                        with open(input_file, "w") as outfile:
                            outfile.writelines(cleaned_lines)
                        
                        print(f"Processing: {input_file}")
                        subprocess.run(["python", REROOT_SCRIPT, input_file], check=True)
                    else:
                        print(f"File not found: {input_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <base_directory>")
        sys.exit(1)

    base_directory = sys.argv[1]
    find_and_reroot(base_directory)
