import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

DU_RATE_LEGENDS = {
    'D18': 'F:1e-18',
    #'D15': 'F:1e-15',
    'D10': 'F:1e-10',
    'D7': 'F:1e-7'
    #'LN0.1': 'LN:(U:-25,-15),0.1',
    #'LN0.3': 'LN:(U:-25,-15),0.3',
}

def plot_linear(csv_file1):
    # Set global font size to 18
    plt.rcParams.update({'font.size': 18})

    # Read both CSV files
    df1 = pd.read_csv(csv_file1)
    
    # Extract data for the first file
    x_values1 = df1.iloc[:, -1].values  # Last column as x-values (names)
    names1 = df1.columns[1:-1]  # Names for the curves from the columns (excluding the first and last columns)

    # Get the base file names without extension
    base_name1 = os.path.splitext(os.path.basename(csv_file1))[0]
    
    # Modify x-axis labels based on DU_RATE_LEGENDS for the first file
    x_labels1 = []
    for label in x_values1:
        label = str(label)  # Ensure the label is a string
        pos = label.find("Duprate")
        if pos != -1:
            label = label[pos:]
        custom_label = DU_RATE_LEGENDS.get(label, label)
        x_labels1.append(custom_label)
    
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    recall = False
    # Plot curves from the first file
    for name in names1:
        y_values = df1[name].values  # Get y-values for the linear plot
        if name == 'out_lca_improvedTreesDL_b1000_90_1_recall':
            recall = True
        if name == 'lca_recall' or name == 'lca_precision' or name == 'lca_FP':
            plt.plot(x_labels1, y_values, marker='o', label=f'LCA (1 WGD)', linestyle='-', color='#ff000e')  # Solid line for 'lca_recall'
        elif name == 'greedydown100_recall' or name == 'greedydown100_precision' or name == 'greedydown100_FP':
            plt.plot(x_labels1, y_values, marker='o', label=f'FastMultRec (1 WGD)', linestyle=':', color='#1100ff')  # Dashed line for others
        
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
    pdf_file = os.path.join('plots', f'{base_name1}.pdf')
    plt.savefig(pdf_file, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file1>")
        sys.exit(1)
    
    csv_file1 = sys.argv[1]
    plot_linear(csv_file1)
