import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Function to plot data from the given files
def plot_data(file_list, ax, legend_suffix):
    custom_colors = ['red', 'blue']

    for idx, file in enumerate(file_list):
        if os.path.exists(file):
            data = pd.read_csv(file)
            label = file.split('/')[-1].split('.')[0]  # Use the file name without directory and extension
            ax.plot(data.iloc[:, 0], data.iloc[:, 1], 
                    label=f"{label} {legend_suffix}" if legend_suffix else label, 
                    linewidth=1, color=custom_colors[idx % len(custom_colors)], alpha=0.5)
    
    ax.set_xticks([])  # Remove x-axis values

# Function to generate plots for a single subdirectory
def generate_plots_for_subdir(subdir):
    # List of i values
    i_values = [4, 5]
    
    # Create a figure for the subdirectory
    fig, axes = plt.subplots(4, 2, figsize=(20, 30))  # 4 rows, 2 columns
    fig.suptitle(f"Combined Plots for {subdir}")

    # First row: lca and simphy
    simphy_file = os.path.join(subdir, 'out_simphy.txt.csv')
    lca_file = os.path.join(subdir, 'out_lca.txt.csv')
    plot_data([lca_file, simphy_file], axes[0, 0], '')
    axes[0, 0].legend()
    axes[0, 0].set_title('LCA vs Simphy')

    # Second row: greedy 4 and greedy 5
    for i in i_values:
        variable_file = os.path.join(subdir, f'out_greedy{i}.txt.csv')
        plot_data([variable_file, simphy_file], axes[1, i - 4], '')
        axes[1, i - 4].legend()
        axes[1, i - 4].set_title(f'Greedy without Down moves {i}')

    # Third row: greedy down 4 and 5
    for i in i_values:
        variable_file = os.path.join(subdir, f'out_greedydown{i}.txt.csv')
        plot_data([variable_file, simphy_file], axes[2, i - 4], '')
        axes[2, i - 4].legend()
        axes[2, i - 4].set_title(f'Greedy with Down moves {i}')

    # Fourth row: stochastic 4 and 5
    for i in i_values:
        variable_file = os.path.join(subdir, f'out_stochastic{i}.txt.csv')
        plot_data([variable_file, simphy_file], axes[3, i - 4], '')
        axes[3, i - 4].legend()
        axes[3, i - 4].set_title(f'Stochastic {i}')

    # Remove empty subplots
    for ax in axes.flat:
        if not ax.has_data():
            ax.remove()

    return fig

# Main function to generate plots for all subdirectories and save them as a single PDF
def generate_plots(directory):
    os.chdir(directory)
    subdirs = [f"sim_{i}" for i in range(1, 101)]

    with PdfPages(f"{os.path.basename(directory)}.pdf") as pdf:
        for subdir in subdirs:
            if os.path.exists(subdir):
                fig = generate_plots_for_subdir(subdir)
                pdf.savefig(fig)
                plt.close(fig)

# Usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    generate_plots(directory)
