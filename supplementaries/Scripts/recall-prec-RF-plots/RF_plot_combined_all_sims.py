import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

def plot_combined_box(sim_0WGD_dir, t_values, d_values, output_pdf):
    data = []
    labels = []

    for t in t_values:
        for d in d_values:
            combined_rf_values = []

            for i in range(1, 26):
                sim_i_path = os.path.join(sim_0WGD_dir, f"sim_{i}")
                rf_csv_t_d = os.path.join(sim_i_path, f"rf_dist_{t}_{d}.csv")

                if os.path.exists(rf_csv_t_d):
                    df_t_d = pd.read_csv(rf_csv_t_d)
                    combined_rf_values.extend(df_t_d.iloc[:, 1])  # Collect RF distances (2nd column)
                else:
                    print(f"Warning: {rf_csv_t_d} not found, skipping.")

            if combined_rf_values:
                data.append(combined_rf_values)
                labels.append(f"{t}_{d}")

    if not data:
        print(f"No RF data files found in {sim_0WGD_dir}, skipping box plot.")
        return

    plt.figure(figsize=(10, 6))
    plt.boxplot(data, vert=True, patch_artist=True)
    plt.xticks(range(1, len(labels) + 1), labels)
    plt.ylabel("RF Distance")
    plt.title("Combined Box Plot of RF Distances (all sim_i, t_d combinations)")
    plt.tight_layout()
    plt.savefig(output_pdf)
    plt.close()
    print(f"Combined box plot saved: {output_pdf}")

if __name__ == "__main__":
    sim_0WGD_dir = sys.argv[1]
    output_pdf = sys.argv[2]

    # Parameters to plot
    t_values = [50, 70, 90, 95]
    d_values = [1, 5]

    plot_combined_box(sim_0WGD_dir, t_values, d_values, output_pdf)
