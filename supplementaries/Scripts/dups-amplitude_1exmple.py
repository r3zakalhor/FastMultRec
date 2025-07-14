import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

# Function to plot data from the given files
def plot_difference(file1, file2, ax, label, color, linestyle='-', scatter_color=None, label_sc=''):
    if os.path.exists(file1) and os.path.exists(file2):
        data1 = pd.read_csv(file1)
        data2 = pd.read_csv(file2)
        
        # Ensure both dataframes have the same length
        if len(data1) == len(data2):
            difference = data1.iloc[:, 1] - data2.iloc[:, 1]
            ax.plot(data1.iloc[:, 0], difference, label=label, color=color, linestyle=linestyle, linewidth=1)
            sum_of_differences = difference.sum()
            #ax.annotate(f'Sum: {sum_of_differences:.2f}', 
                        #xy=(0.45, 0.97), xycoords='axes fraction', fontsize=10,
                        #verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'))
            
            # Highlight points where simphy value > 20
            #highlight_10 = data2.iloc[:, 1] > 20
            #ax.scatter(data1.iloc[:, 0][highlight_10], difference[highlight_10], color=scatter_color, zorder=5, label=f'{label} (Gis > 20)')

            # Highlight points where simphy value > 80 with a '*' marker
            highlight_50 = data2.iloc[:, 1] > 80
            ax.scatter(data1.iloc[:, 0][highlight_50], difference[highlight_50], color=scatter_color, s=100, zorder=6, label='WGD')

    ax.set_ylim(-100, 100)  # Set fixed y-axis values
    
    ax.set_xticks([])  # Remove x-axis values

# Function to generate a single plot for the subdirectory
def generate_single_plot_for_subdir(subdir):
    # Create a single figure
    plt.figure(figsize=(12, 8))
    fig, ax = plt.subplots(figsize=(10, 6))  # Single subplot
    
    simphy_file = os.path.join(subdir, 'out_simphy.txt.csv')
    lca_file = os.path.join(subdir, 'out_lca.txt.csv')
    greedy100_file = os.path.join(subdir, 'out_greedy100.txt.csv')

    # Plot the LCA - Simphy difference with specific color and scatter color
    #plot_difference(lca_file, simphy_file, ax, 'LCA - SimPhy', color='#1100ff', scatter_color='#1100ff', label_sc='LCA')

    # Plot the Greedy 100 - Simphy difference with specific color, line style, and scatter color
    plot_difference(greedy100_file, simphy_file, ax, 'Our approach - SimPhy', color='#ff000e', linestyle='-', scatter_color='#ff000e', label_sc='Our approach')
    plt.yticks(fontsize=17)  # y-tick labels
    plt.ylim(-100, 100)
    steps = np.arange(-100, 101, 100)  # From -10 to 10 with a step of 2
    plt.yticks(steps)
    ax.legend(fontsize=20)  # Set legend font size
    
    #ax.set_title(f'Amplitude Plot for {subdir}', fontsize=18)  # Title font size
    ax.set_xlabel("Species", fontsize=20, labelpad=50)  # X-axis label font size
    ax.set_ylabel("Amplitude", fontsize=20)  # Y-axis label font size  
    # Move spines to the center
    ax.spines['left'].set_position('zero')   # Move the y-axis spine to the center
    ax.spines['bottom'].set_position('zero') # Move the x-axis spine to the center
    ax.spines['bottom'].set_zorder(0)
    ax.spines['bottom'].set_color('gray')
    ax.spines['bottom'].set_linestyle('--')  # Set dotted line style
    ax.spines['bottom'].set_linewidth(0.5)   # You can adjust the line width if needed
    # Hide the top and right spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    # Adjust the ticks to only show on bottom and left spines
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')    # Adjust layout to remove white space
    plt.tight_layout()  
    return fig

# Main function to generate the plot for a specific subdirectory
def generate_plot_for_subdir(directory, subdir_number):
    subdir = f"sim_{subdir_number}"
    if os.path.exists(subdir):
        with PdfPages(f"{os.path.basename(directory)}-amp-{subdir_number}.pdf") as pdf:
            fig = generate_single_plot_for_subdir(subdir)
            pdf.savefig(fig)
            plt.close(fig)
    else:
        print(f"Subdirectory {subdir} does not exist.")

# Usage
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <directory> <subdir_number>")
        sys.exit(1)
    
    directory = sys.argv[1]
    subdir_number = sys.argv[2]  # Get the subdirectory number from arguments
    os.chdir(directory)
    generate_plot_for_subdir(directory, subdir_number)
