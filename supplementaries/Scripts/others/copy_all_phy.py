import os
import shutil

def organize_phy_files():
    # Create the 'sequences' directory if it doesn't exist
    sequences_dir = "trees_0WGD"
    os.makedirs(sequences_dir, exist_ok=True)
    
    # Find directories starting with 'sim_0WGD'
    for sim_0wgd in sorted([d for d in os.listdir() if d.startswith("sim_0WGD") and os.path.isdir(d)]):
        sim_0wgd_path = os.path.join(sequences_dir, sim_0wgd)
        os.makedirs(sim_0wgd_path, exist_ok=True)
        
        # Iterate over sim_x directories (x from 1 to 25)
        for x in range(1, 26):
            sim_x = f"sim_{x}"
            src_sim_x_path = os.path.join(sim_0wgd, sim_x)
            dest_sim_x_path = os.path.join(sim_0wgd_path, sim_x)
            
            if os.path.isdir(src_sim_x_path):
                os.makedirs(dest_sim_x_path, exist_ok=True)
                
                # Copy all .phy files to the corresponding destination
                for phy_file in os.listdir(src_sim_x_path):
                    if phy_file.endswith("applied_loss_fix_all_genetrees_edited.txt") or phy_file.endswith("applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree_rerooted.txt"):
                        src_file = os.path.join(src_sim_x_path, phy_file)
                        dest_file = os.path.join(dest_sim_x_path, phy_file)
                        shutil.copy2(src_file, dest_file)
                        print(f"Copied {src_file} -> {dest_file}")

if __name__ == "__main__":
    organize_phy_files()
