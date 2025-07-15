import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

DU_RATE_LEGENDS = {
    '_D18': 'F:1e-18',
    '_D10': 'F:1e-10',
    '_D7': 'F:1e-7'
}

def plot_linear(recall_files, precision_files):
    # Set global font size to 18
    plt.rcParams.update({'font.size': 18})

    # Create a figure with 2 rows and 4 columns (1x4 grid for each recall and precision)
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs = axs.ravel()  # Flatten the 2x4 array of axes for easier indexing
    
    thresholds = ['t50', 't80']
    threshold_labels = ['Threshold 50', 'Threshold 80']
    
    # Loop over the recall and precision CSV files and thresholds
    for idx, (recall_file, precision_file, threshold) in enumerate(zip(recall_files, precision_files, thresholds)):
        # First row (recall plots)
        ax_recall = axs[idx]  # Recall axes for the first row
        # Read the recall CSV file for the current threshold
        df_recall = pd.read_csv(recall_file)
        
        # Extract data
        directory_values = df_recall['directory'].values  # Get the 'directory' column values
        names_recall = df_recall.columns[1:-1]  # Names for the recall curves from the columns (excluding the first and last columns)

        # Modify x-axis labels based on DU_RATE_LEGENDS for the 'directory' column
        x_labels1 = []
        for label in directory_values:
            label = str(label)  # Ensure it's a string
            pos = label.find("_D")  # Find the position of "_D"
            if pos != -1:
                label = label[pos:]  # Extract the substring starting from "_D"
            custom_label = DU_RATE_LEGENDS.get(label, label)  # Replace using the dictionary
            x_labels1.append(custom_label)

        # Plot recall curves
        for name in names_recall:
            y_values = df_recall[name].values  # Get y-values for the linear plot
            #if name == 'out_lca_improvedTreesDL_b1000_90_1_recall':
            if name == 'out_lca_improvedTreesDL_b1000_unclean_recall':
                ax_recall.plot(x_labels1, y_values, marker='o', label=f'LCA (2 WGD)', linestyle='-', color='#ff000e')
            elif name == 'out_greedydown100_improvedTreesDL_b1000_unclean_recall':
                ax_recall.plot(x_labels1, y_values, marker='o', label=f'FastMultRec (2 WGD)', linestyle=':', color='#1100ff')
            elif name == 'MetaEc_out_recall':
                ax_recall.plot(x_labels1, y_values, marker='o', label='MetaEC (2 WGD)', linestyle='--', color='#008000')


        # Set y-axis limits from 0 to 1 for recall
        ax_recall.set_ylim(0, 1)

        # Set labels, title, and legend for recall subplot
        #ax_recall.set_xlabel('D & L Rate', fontsize=14)
        if idx == 0:
            ax_recall.set_ylabel('Recall', fontsize=20)  # Only set ylabel for the leftmost plot
            ax_recall.legend(fontsize=18)
        else:
            ax_recall.set_ylabel('')  # Remove y-axis labels for all other plots
        ax_recall.set_title(f"{threshold_labels[idx]}", fontsize=20)
        

        # Update x-axis labels for recall
        ax_recall.set_xticks([])  # Ensure the correct number of ticks
        ax_recall.set_xticklabels([])  # Apply custom x-axis labels and rotate them

        # Second row (precision plots)
        ax_precision = axs[idx + 2]  # Precision axes for the second row
        # Read the precision CSV file for the current threshold
        df_precision = pd.read_csv(precision_file)
        
        # Extract data
        names_precision = df_precision.columns[1:-1]  # Names for the precision curves

        # Plot precision curves
        for name in names_precision:
            y_values = df_precision[name].values  # Get y-values for the linear plot
            if name == 'out_lca_improvedTreesDL_b1000_unclean_precision':
                ax_precision.plot(x_labels1, y_values, marker='o', label=f'LCA ({threshold_labels[idx]})', linestyle='-', color='#ff000e')
            elif name == 'out_greedydown100_improvedTreesDL_b1000_unclean_precision':
                ax_precision.plot(x_labels1, y_values, marker='o', label=f'FastMultRec ({threshold_labels[idx]})', linestyle=':', color='#1100ff')
            elif name == 'MetaEc_out_precision':
                ax_precision.plot(x_labels1, y_values, marker='o', label='MetaEC (2 WGD)', linestyle='--', color='#008000')


        # Set y-axis limits from 0 to 1 for precision
        ax_precision.set_ylim(0, 1.01)

        # Set labels, title, and legend for precision subplot
        ax_precision.set_xlabel('D & L Rate', fontsize=20)
        if idx == 0:
            ax_precision.set_ylabel('Precision', fontsize=20)  # Only set ylabel for the leftmost plot in the second row
        else:
            ax_precision.set_ylabel('')  # Remove y-axis labels for all other plots
        #ax_precision.set_title(f"Precision {threshold_labels[idx]}", fontsize=16)
        #ax_precision.legend(fontsize=12)

        # Update x-axis labels for precision
        ax_precision.set_xticks(range(len(x_labels1)))  # Ensure the correct number of ticks
        ax_precision.set_xticklabels(x_labels1, rotation=90)  # Apply custom x-axis labels and rotate them

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Ensure 'plots' directory exists
    if not os.path.exists('plots'):
        os.makedirs('plots')

    # Save plot as PDF with a combined name of the CSV files
    pdf_file = os.path.join('plots', 'comparison_thresholds_both_rows.pdf')
    plt.savefig(pdf_file, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usage: python script.py <recall_file_t50> <recall_file_t60> <recall_file_t70> <recall_file_t80> <precision_file_t50> <precision_file_t60> <precision_file_t70> <precision_file_t80>")
        sys.exit(1)
    
    # Accept four recall CSV file paths and four precision CSV file paths as command-line arguments
    #recall_files = [
    #    "recall-1W-WGD-improvedtrees-bootstrap-b1000-2NumApp-t50-t200-Avg.csv",
    #    "recall-1W-WGD-improvedtrees-bootstrap-b1000-2NumApp-t80-t200-Avg.csv"]
    #precision_files = [
    #    "precision-1W-WGD-improvedtrees-bootstrap-b1000-2NumApp-t50-t200-Avg.csv",
    #    "precision-1W-WGD-improvedtrees-bootstrap-b1000-2NumApp-t80-t200-Avg.csv"]

    #recall_files = [
    #    "recall-2W-WGD-improvedtrees-bootstrap-b1000-2NumApp-Metaec-t50-t200-Avg.csv",
    #    "recall-2W-WGD-improvedtrees-bootstrap-b1000-2NumApp-Metaec-t80-t200-Avg.csv"]
    #precision_files = [
    #    "precision-2W-WGD-improvedtrees-bootstrap-b1000-2NumApp-Metaec-t50-t200-Avg.csv",
    #    "precision-2W-WGD-improvedtrees-bootstrap-b1000-2NumApp-Metaec-t80-t200-Avg.csv"]


    #recall_files = [
    #    "recall-2W-WGD-improvedtrees-bootstrap-b1000-unclean-t20-t50-Avg.csv",
    #    "recall-2W-WGD-improvedtrees-bootstrap-b1000-unclean-t20-t80-Avg.csv"]
    #precision_files = [
    #    "precision-2W-WGD-improvedtrees-bootstrap-b1000-unclean-t20-t50-Avg.csv",
    #    "precision-2W-WGD-improvedtrees-bootstrap-b1000-unclean-t20-t80-Avg.csv"]

    recall_files = [
        "recall-2W-WGD-unclean-2NumApp-Metaec-t50-t200-Avg.csv",
        "recall-2W-WGD-unclean-2NumApp-Metaec-t80-t200-Avg.csv"]
    precision_files = [
        "precision-2W-WGD-unclean-2NumApp-Metaec-t50-t200-Avg.csv",
        "precision-2W-WGD-unclean-2NumApp-Metaec-t80-t200-Avg.csv"]

    plot_linear(recall_files, precision_files)
