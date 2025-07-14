import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_line(df, output_pdf):
    plt.figure()
    plt.plot(df.iloc[:, 0], df.iloc[:, 1], marker='o', linestyle='-')
    plt.xlabel("Tree Number")
    plt.ylabel("RF Distance")
    plt.title("RF Distance Line Plot")
    plt.tight_layout()
    plt.savefig(output_pdf)
    plt.close()

def plot_combined_box(sim_i_path, t_values, d_values, output_pdf):
    data = []
    labels = []
    
    for t in t_values:
        for d in d_values:
            rf_csv_t_d = os.path.join(sim_i_path, f"rf_dist_{t}_{d}.csv")
            if os.path.exists(rf_csv_t_d):
                df_t_d = pd.read_csv(rf_csv_t_d)
                data.append(df_t_d.iloc[:, 1])  # Assuming RF values are in second column
                labels.append(f"{t}_{d}")
            else:
                print(f"Warning: File {rf_csv_t_d} not found, skipping.")

    if not data:
        print(f"No RF data files found in {sim_i_path}, skipping box plot.")
        return

    plt.figure(figsize=(10, 6))
    plt.boxplot(data, vert=True, patch_artist=True)
    plt.xticks(range(1, len(labels) + 1), labels)
    plt.ylabel("RF Distance")
    plt.title("Box Plot of RF Distances (t_d combinations)")
    plt.tight_layout()
    plt.savefig(output_pdf)
    plt.close()

if __name__ == "__main__":
    csv_file = sys.argv[1]
    #line_pdf = sys.argv[2]
    box_pdf = sys.argv[2]

    # Get sim_i directory path from csv_file path
    sim_i_path = os.path.dirname(csv_file)

    # Parameters you want to test
    t_values = [50, 70, 90, 95]
    d_values = [1, 5]

    df = pd.read_csv(csv_file)
    #plot_line(df, line_pdf)
    plot_combined_box(sim_i_path, t_values, d_values, box_pdf)
