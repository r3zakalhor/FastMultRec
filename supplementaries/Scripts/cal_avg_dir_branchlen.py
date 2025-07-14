import os
import csv
import subprocess
import numpy as np
import glob

def process_sim_directories():
    """Processes all sim_1WGD* directories and calculates average tree height & branch length for each sim_i."""
    
    sim_1WGD_dirs = sorted(glob.glob("sim_1WGD*"))  # Get all directories starting with sim_1WGD
    
    for sim_1WGD in sim_1WGD_dirs:
        results = []
        
        for i in range(1, 26):  # Loop over sim_1WGD*/sim_i where i is 1 to 25
            sim_i_path = os.path.join(sim_1WGD, f"sim_{i}")
            input_file = os.path.join(sim_i_path, "applied_loss_fix_all_genetrees_edited.txt")
            output_csv = input_file.replace(".txt", ".csv")  # Expected output CSV filename

            if os.path.exists(input_file):  # Check if input file exists
                print(f"Processing: {input_file}")
                
                # Run the TreeHeight_AvgBranchLen.py script
                subprocess.run(["python", "TreeHeight_AvgBranchLen.py", input_file], check=True)

                # Extract values from CSV
                if os.path.exists(output_csv):  # Ensure CSV was created
                    tree_heights = []
                    branch_lengths = []

                    with open(output_csv, 'r') as csvfile:
                        reader = csv.reader(csvfile)
                        next(reader)  # Skip header
                        for row in reader:
                            tree_heights.append(float(row[1]))  # Second column: Tree height
                            branch_lengths.append(float(row[2]))  # Third column: Avg branch length
                    
                    # Compute averages
                    avg_height = np.mean(tree_heights) if tree_heights else 0
                    avg_branch = np.mean(branch_lengths) if branch_lengths else 0

                    results.append([f"sim_{i}", avg_height, avg_branch])

        # Save results in a CSV file in sim_1WGD*
        output_summary = os.path.join(sim_1WGD, "summary_avg_tree_metrics.csv")
        with open(output_summary, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Simulation", "Avg Tree Height", "Avg Branch Length"])
            writer.writerows(results)
        
        print(f"Summary saved: {output_summary}")

if __name__ == "__main__":
    process_sim_directories()
