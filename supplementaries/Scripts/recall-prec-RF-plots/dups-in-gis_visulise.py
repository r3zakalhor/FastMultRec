import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Function to plot data from the given files
def plot_data(file_list, ax, legend_suffix):
    # Define a custom color palette with red and blue
    custom_colors = ['red', 'blue']
    
    for idx, file in enumerate(file_list):
        if os.path.exists(file):
            data = pd.read_csv(file)
            label = file.split('.')[0].split('_')[1] if 'greedy' in file or 'stochastic' in file else file.split('.')[0].split('_')[1]
            
            # Plot with narrower bars and red/blue colors
            ax.plot(data.iloc[:, 0], data.iloc[:, 1], label=f"{label} {legend_suffix}" if 'greedy' in file or 'stochastic' in file else label, 
                    linewidth=1, color=custom_colors[idx % len(custom_colors)], alpha=0.5)
    
    ax.set_xticks([])  # Remove x-axis values

# Main function to generate plots and save them as PDF
def generate_plots(directory):
    os.chdir(directory)
    
    # List of i values
    i_values = [2, 3, 4, 5, 10, 20, 30, 50, 70, 100]
    
    # Prepare lists of files for each page
    file_sets = [
        ('out_greedyi.txt.csv', 'Greedy'),
        ('out_greedydowni.txt.csv', 'Greedy Down'),
        ('out_stochastici.txt.csv', 'Stochastic')
    ]
    
    # Create PDF with multiple pages
    with PdfPages(f"{os.path.basename(directory)}.pdf") as pdf:
        for file_suffix, plot_type in file_sets:
            fig, axes = plt.subplots(4, 3, figsize=(15, 20))  # 4x3 grid
            fig.suptitle(f"{plot_type} Plots")
            
            # First subplot with 'lca' and 'simphy'
            simphy_file = 'out_simphy.txt.csv'
            lca_file = 'out_lca.txt.csv'
            file_list = [lca_file, simphy_file]
            plot_data(file_list, axes[0, 0], '')
            axes[0, 0].legend()
            axes[0, 0].set_xlabel('Species ID')
            axes[0, 0].set_ylabel('Num Gis')
            
            # Remaining subplots for 'greedy' or 'stochastic'
            for idx, i in enumerate(i_values):
                if file_suffix == 'out_stochastici.txt.csv':
                    index = file_suffix.find('stochastic') + len('stochastic')
                    variable_file = file_suffix[:index] + str(i) + file_suffix[index + 1:]                    
                else:
                    variable_file = file_suffix.replace('i', str(i))
                
                file_list = [variable_file, simphy_file]
                # Calculate the correct row and column indices for subplots
                row = (idx + 1) // 3
                col = (idx + 1) % 3
                plot_data(file_list, axes[row, col], i)
                axes[row, col].legend()
                axes[row, col].set_xlabel('Species ID')
                axes[row, col].set_ylabel('Num Gis')
            
            # Remove the last subplot in the 4x3 grid
            fig.delaxes(axes[3, 2])
            
            pdf.savefig(fig)
            plt.close(fig)

# Usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    generate_plots(directory)
