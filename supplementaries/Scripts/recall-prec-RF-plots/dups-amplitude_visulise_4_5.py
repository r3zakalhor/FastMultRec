import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Function to plot data from the given files
def plot_difference(file1, file2, ax, label):
    if os.path.exists(file1) and os.path.exists(file2):
        data1 = pd.read_csv(file1)
        data2 = pd.read_csv(file2)
        
        # Ensure both dataframes have the same length
        if len(data1) == len(data2):
            difference = data1.iloc[:, 1] - data2.iloc[:, 1]
            ax.plot(data1.iloc[:, 0], difference, label=label, linewidth=1)
            sum_of_differences = difference.sum()
            ax.annotate(f'Sum: {sum_of_differences:.2f}', 
                        xy=(0.45, 0.97), xycoords='axes fraction', fontsize=10,
                        verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'))
            
            # Highlight points where simphy value > 20
            highlight_10 = data2.iloc[:, 1] > 20
            ax.scatter(data1.iloc[:, 0][highlight_10], difference[highlight_10], color='red', zorder=5, label='Gis > 20')

            # Highlight points where simphy value > 80 with a '*' marker
            highlight_50 = data2.iloc[:, 1] > 80
            ax.scatter(data1.iloc[:, 0][highlight_50], difference[highlight_50], color='blue', marker='*', s=100, zorder=6, label='Gis > 80')

    ax.set_ylim(-100, 100)  # Set fixed y-axis values
    ax.set_xticks([])  # Remove x-axis values

# Function to generate plots for a single subdirectory
def generate_plots_for_subdir(subdir):
    # List of i values
    i_values = [5, 100]
    
    # Create a figure for the subdirectory
    fig, axes = plt.subplots(4, 2, figsize=(20, 30))  # 4 rows, 2 columns
    fig.suptitle(f"Amplitude Plots for {subdir}")

    # First row: lca - simphy and simphy - simphy (should be zero)
    simphy_file = os.path.join(subdir, 'out_simphy.txt.csv')
    lca_file = os.path.join(subdir, 'out_lca.txt.csv')
    plot_difference(lca_file, simphy_file, axes[0, 0], 'LCA - SimPhy')
    axes[0, 0].legend()
    axes[0, 0].set_title('LCA - Simphy')
    axes[0, 0].set_xlabel("Species")
    axes[0, 0].set_ylabel("Amplitude")

    # Second row: greedy 5 - simphy and greedy 100 - simphy
    for index, i in enumerate(i_values):
        variable_file = os.path.join(subdir, f'out_greedy{i}.txt.csv')
        plot_difference(variable_file, simphy_file, axes[1, index], f'Greedy (d{i}) - SimPhy')
        axes[1, index].legend()
        axes[1, index].set_title(f'Greedy {i} - Simphy')
        axes[1, index].set_xlabel("Species")
        axes[1, index].set_ylabel("Amplitude")

    # Third row: greedy down 5 - simphy and greedy down 100 - simphy
    for index, i in enumerate(i_values):
        variable_file = os.path.join(subdir, f'out_greedydown{i}.txt.csv')
        plot_difference(variable_file, simphy_file, axes[2, index], f'Our approach (d{i}) - SimPhy')
        axes[2, index].legend()
        axes[2, index].set_title(f'Our approach {i} - Simphy')
        axes[2, index].set_xlabel("Species")
        axes[2, index].set_ylabel("Amplitude")

    # Fourth row: stochastic 5 - simphy and stochastic 100 - simphy
    for index, i in enumerate(i_values):
        variable_file = os.path.join(subdir, f'out_stochastic{i}.txt.csv')
        plot_difference(variable_file, simphy_file, axes[3, index], f'Stochastic (d{i}) - SimPhy')
        axes[3, index].legend()
        axes[3, index].set_title(f'Stochastic {i} - Simphy')
        axes[3, index].set_xlabel("Species")
        axes[3, index].set_ylabel("Amplitude")

    # Remove empty subplots
    for ax in axes.flat:
        if not ax.has_data():
            ax.remove()

    return fig

# Main function to generate plots for all subdirectories and save them as a single PDF
def generate_plots(directory):
    os.chdir(directory)
    subdirs = [f"sim_{i}" for i in range(1, 101)]

    with PdfPages(f"{os.path.basename(directory)}-amp.pdf") as pdf:
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
