import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

DU_RATE_LEGENDS = {
    'Duprate-18': 'F:1e-18',
    #'Duprate-15': 'F:1e-15',
    #'Duprate-11': 'F:1e-11',
    'Duprate-10': 'F:1e-10',
    #'Duprate-9': 'F:1e-9',
    #'Duprate-8': 'F:1e-8',
    'Duprate-7': 'F:1e-7'
    #'Duprate-6': 'F:1e-6',
    #'Duprate_u-gb_0.1': 'LN:(U:-25,-15),0.1',
    #'Duprate_u-gb_0.3': 'LN:(U:-25,-15),0.3',
    #'Duprate_u-gb_1': 'LN:(U:-25,-15),1',
    #'Duprate_u-6_-12': 'U:1e-6,1e-12'
}

def plot_linear(csv_file1, csv_file2):
    # Set global font size to 18
    plt.rcParams.update({'font.size': 18})

    # Read both CSV files
    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)
    
    # Extract data for the first file
    x_values1 = df1.iloc[:, -1].values  # Last column as x-values (names)
    names1 = df1.columns[1:-1]  # Names for the curves from the columns (excluding the first and last columns)

    # Extract data for the second file
    x_values2 = df2.iloc[:, -1].values  # Last column as x-values (names)
    names2 = df2.columns[1:-1]  # Names for the curves from the columns (excluding the first and last columns)

    # Get the base file names without extension
    base_name1 = os.path.splitext(os.path.basename(csv_file1))[0]
    base_name2 = os.path.splitext(os.path.basename(csv_file2))[0]
    
    # Modify x-axis labels based on DU_RATE_LEGENDS for the first file
    x_labels1 = []
    for label in x_values1:
        label = str(label)  # Ensure the label is a string
        pos = label.find("Duprate")
        if pos != -1:
            label = label[pos:]
        custom_label = DU_RATE_LEGENDS.get(label, label)
        x_labels1.append(custom_label)
    
    # Modify x-axis labels based on DU_RATE_LEGENDS for the second file
    x_labels2 = []
    for label in x_values2:
        label = str(label)  # Ensure the label is a string
        pos = label.find("Duprate")
        if pos != -1:
            label = label[pos:]
        custom_label = DU_RATE_LEGENDS.get(label, label)
        x_labels2.append(custom_label)
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    recall = False
    # Plot curves from the first file
    for name in names1:
        y_values = df1[name].values  # Get y-values for the linear plot
        if name == 'out_lca_improvedTreesDL_b1000_90_1_recall':
            recall = True
        if name == 'out_lca_improvedTreesDL_b1000_90_1_recall' or name == 'out_lca_improvedTreesDL_b1000_90_1_precision':
            plt.plot(x_labels1, y_values, marker='o', label=f'LCA (1 WGD)', linestyle='-', color='#ff000e')  # Solid line for 'lca_recall'
        elif name == 'out_greedydown100_improvedTreesDL_b1000_90_1_recall' or name == 'out_greedydown100_improvedTreesDL_b1000_90_1_precision':
            plt.plot(x_labels1, y_values, marker='o', label=f'Our approach (1 WGD)', linestyle=':', color='#1100ff')  # Dashed line for others
    
    # Plot curves from the second file
    for name in names2:
        y_values = df2[name].values  # Get y-values for the linear plot
        if name == 'out_lca_improvedTreesDL_b1000_90_1_recall':
            recall = True
        if name == 'out_lca_improvedTreesDL_b1000_90_1_recall' or name == 'out_lca_improvedTreesDL_b1000_90_1_precision':
            plt.plot(x_labels2, y_values, marker='x', label=f'LCA (2 WGD)', linestyle='-', color='#ff000e')  # Dotted line for 'lca_recall' from the second file
        elif name == 'out_greedydown100_improvedTreesDL_b1000_90_1_recall' or name == 'out_greedydown100_improvedTreesDL_b1000_90_1_precision':
            plt.plot(x_labels2, y_values, marker='x', label=f'Our approach (2 WGD)', linestyle=':', color='#1100ff')  # Dotted line for others from the second file
    
    # Set x and y labels, legends, and ticks font sizes
    plt.xticks(rotation=90, fontsize=18)  # x-tick labels
    plt.yticks(fontsize=18)  # y-tick labels
    #plt.ylim(0, 1.05)
    plt.xlabel('D & L Rate', fontsize=18)
    if recall:
        plt.ylabel('Recall', fontsize=18)
    else:
        plt.ylabel('Precision', fontsize=18)
    
    # Set legend font size
    plt.legend(fontsize=18)
    
    # Ensure 'plots' directory exists
    if not os.path.exists('plots'):
        os.makedirs('plots')
    
    # Save plot as PDF with a combined name of both CSV files
    pdf_file = os.path.join('plots', f'{base_name1}_{base_name2}.pdf')
    plt.savefig(pdf_file, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <csv_file1> <csv_file2>")
        sys.exit(1)
    
    csv_file1 = sys.argv[1]
    csv_file2 = sys.argv[2]
    plot_linear(csv_file1, csv_file2)
