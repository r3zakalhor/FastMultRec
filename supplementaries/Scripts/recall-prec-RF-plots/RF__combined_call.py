import os
import subprocess

def call_combined_box_plot(sim_0WGD_dir):
    combined_box_pdf = os.path.join(sim_0WGD_dir, f"rf_combined_box_{os.path.basename(sim_0WGD_dir)}.pdf")
    subprocess.run(["python", "RF_plot_combined_all_sims.py", sim_0WGD_dir, combined_box_pdf], check=True)
    print(f"Combined box plot generated: {combined_box_pdf}")

if __name__ == "__main__":
    # Example: change this to your target directory
    target_dir = "sim_1WGD_D7"
    call_combined_box_plot(target_dir)
