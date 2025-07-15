import os
import glob
import subprocess
from PyPDF2 import PdfMerger

def process_rf_analysis():
    # Find all directories starting with sim_1WGD_D10 (or adjust your pattern here)
    sim_0WGD_dirs = sorted(glob.glob("sim_1WGD_D7"))

    # Define t and d combinations
    t_values = [50, 70, 90, 95]
    d_values = [1, 5]

    for sim_0WGD in sim_0WGD_dirs:
        rf_pdfs = []  # To store all generated PDF paths for merging

        for i in range(1, 26):  # Loop over sim_1 to sim_25
            sim_i_path = os.path.join(sim_0WGD, f"sim_{i}")

            # Define base file paths
            file1 = os.path.join(sim_i_path, "applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned.txt")
            base_file2 = os.path.join(sim_i_path, "applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree_rerooted_improvedTreesDL_ultrafastb1000_90_1.txt")
            rf_csv = os.path.join(sim_i_path, "rf_dist.csv")
            #rf_line_pdf = os.path.join(sim_i_path, "rf_dist.pdf")
            rf_box_pdf = os.path.join(sim_i_path, "rf_box.pdf")

            if os.path.exists(file1) and os.path.exists(base_file2):
                print(f"Processing: {sim_0WGD}/sim_{i}")

                # Step 1: Compute base RF Distance
                subprocess.run(["python", "RF_distance.py", file1, base_file2, rf_csv], check=True)

                # Step 2: Compute RF Distances for all t/d combinations
                for t in t_values:
                    for d in d_values:
                        file2_t_d = os.path.join(sim_i_path,
                            f"applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree_rerooted_improvedTreesDL_ultrafastb1000_{t}_{d}.txt")
                        rf_csv_t_d = os.path.join(sim_i_path, f"rf_dist_{t}_{d}.csv")

                        if os.path.exists(file2_t_d):
                            subprocess.run(["python", "RF_distance.py", file1, file2_t_d, rf_csv_t_d], check=True)
                        else:
                            print(f"Warning: {file2_t_d} not found, skipping.")

                # Step 3: Generate combined line + box plots
                subprocess.run(["python", "RF_plot_with_box.py", rf_csv, rf_box_pdf], check=True)

                # Step 4: Collect PDFs for merging
                #if os.path.exists(rf_line_pdf):
                    #rf_pdfs.append(rf_line_pdf)
                if os.path.exists(rf_box_pdf):
                    rf_pdfs.append(rf_box_pdf)

        # Step 5: Merge all PDFs into one
        if rf_pdfs:
            merged_pdf_path = os.path.join(sim_0WGD, f"rf_dist_b100_{os.path.basename(sim_0WGD)}.pdf")
            merger = PdfMerger()

            for pdf in rf_pdfs:
                merger.append(pdf)

            merger.write(merged_pdf_path)
            merger.close()
            print(f"Merged PDF saved: {merged_pdf_path}")

if __name__ == "__main__":
    process_rf_analysis()

