import os
import subprocess
import pandas as pd

def find_sim_directories(base_dir):
    """Find directories starting with sim_0WGD."""
    return [d for d in os.listdir(base_dir) if d.startswith("sim_0WGD") and os.path.isdir(os.path.join(base_dir, d))]

def process_simulation(sim_dir, base_dir, script_path):
    """Process subdirectories sim_1 to sim_25 inside a given sim_0WGD directory."""
    summary_files = []
    
    for i in range(1, 26):
        sub_dir = os.path.join(base_dir, sim_dir, f"sim_{i}")
        if not os.path.exists(sub_dir):
            continue
        
        file1 = os.path.join(sub_dir, "out_greedydown100.txt")
        file2 = os.path.join(sub_dir, "applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned.txt")
        output_csv = os.path.join(sub_dir, "leaves_len.csv")
        summary_csv = os.path.join(sub_dir, "leaves_len_avg.csv")
        
        if os.path.exists(file1) and os.path.exists(file2):
            subprocess.run(["python", script_path, file1, file2, output_csv, summary_csv])
            summary_files.append((i, summary_csv))
    
    return summary_files

def aggregate_results(summary_files, output_file):
    """Aggregate summary CSV files into one final CSV per sim_0WGD."""
    all_data = []
    
    for sim_i, file in summary_files:
        if os.path.exists(file):
            df = pd.read_csv(file)
            avg_values = df.mean(numeric_only=True).to_dict()
            avg_values["Sim_Index"] = sim_i
            all_data.append(avg_values)
    
    if all_data:
        final_df = pd.DataFrame(all_data)
        final_df = final_df[["Sim_Index", "Avg_Branch_Length", "Avg_Spec_Branch_Length", "Avg_Dup_Branch_Length", "Num_Leaves", "Num_Spec", "Num_Dup"]]
        final_df.to_csv(output_file, index=False)
        print(f"Aggregated results saved to {output_file}")

def main():
    base_dir = "/data/simphy/SimPhy/bin/updated_sims_scripts/"  # Update with the correct path
    script_path = "check_branch_length.py"  # Update if the script path differs
    
    sim_dirs = find_sim_directories(base_dir)
    for sim_dir in sim_dirs:
        summary_files = process_simulation(sim_dir, base_dir, script_path)
        output_file = os.path.join(base_dir, sim_dir, "aggregated_summary.csv")
        aggregate_results(summary_files, output_file)

if __name__ == "__main__":
    main()
    
