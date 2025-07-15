import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

# Label mapping
DU_RATE_LEGENDS = {
    '_D18': 'F:1e-18',
    '_D10': 'F:1e-10',
    '_D7': 'F:1e-7'
}

# Inputs (only t50 and t80)
recall_files_inferred = [
    "recall-1W-WGD-improvedtrees-bootstrap-b1000-2NumApp-t50-t200-Avg.csv",
    "recall-1W-WGD-improvedtrees-bootstrap-b1000-2NumApp-t80-t200-Avg.csv"]

precision_files_inferred = [
    "precision-1W-WGD-improvedtrees-bootstrap-b1000-2NumApp-t50-t200-Avg.csv",
    "precision-1W-WGD-improvedtrees-bootstrap-b1000-2NumApp-t80-t200-Avg.csv"]

recall_files_true = [
    "recall-1W-WGD-true-t50-t200-Avg.csv",
    "recall-1W-WGD-true-t80-t200-Avg.csv"]

precision_files_true = [
    "precision-1W-WGD-true-t50-t200-Avg.csv",
    "precision-1W-WGD-true-t80-t200-Avg.csv"]

#dup_costs = [3, 10, 50, 60, 70, 80, 90, 100]
dup_costs = [100]
threshold_labels = ['t50', 't80']


def extract_xlabels(df):
    x_labels = []
    for label in df['directory'].values:
        label = str(label)
        pos = label.find("_D")
        if pos != -1:
            label = label[pos:]
        custom_label = DU_RATE_LEGENDS.get(label, label)
        x_labels.append(custom_label)
    return x_labels


def plot_page(fig, dup_cost, recall_files, precision_files, inferred):
    axs = fig.subplots(2, 4)
    axs = axs.ravel()

    for idx, (recall_file, precision_file) in enumerate(zip(recall_files, precision_files)):
        ax_recall = axs[idx]
        ax_precision = axs[idx + 4]

        df_recall = pd.read_csv(recall_file)
        df_precision = pd.read_csv(precision_file)
        x_labels = extract_xlabels(df_recall)

        # Column names
        if inferred:
            recall_col = f"out_greedydown{dup_cost}_improvedTreesDL_b1000_90_1_recall"
            precision_col = f"out_greedydown{dup_cost}_improvedTreesDL_b1000_90_1_precision"
            lca_recall_col = "out_lca_improvedTreesDL_b1000_90_1_recall"
            lca_precision_col = "out_lca_improvedTreesDL_b1000_90_1_precision"
        else:
            recall_col = f"out_true_greedydown{dup_cost}_recall"
            precision_col = f"out_true_greedydown{dup_cost}_precision"
            lca_recall_col = "out_true_lca_recall"
            lca_precision_col = "out_true_lca_precision"

        # --- Plot Recall ---
        if recall_col in df_recall.columns:
            ax_recall.plot(x_labels, df_recall[recall_col], marker='o', linestyle=':', color='#1100ff', label="FastMultRec (1 WGD)")

        if lca_recall_col in df_recall.columns:
            ax_recall.plot(x_labels, df_recall[lca_recall_col], marker='s', linestyle='-', color='#ff000e', label="LCA (1 WGD)")

        ax_recall.set_ylim(0, 1.02)
        if idx == 0:
            ax_recall.set_ylabel("Recall", fontsize=20)
            #ax_recall.legend(fontsize=18)
        else:
            ax_recall.set_ylabel("")
        ax_recall.set_title(threshold_labels[idx], fontsize=20)
        ax_recall.set_xticks(range(len(x_labels)))
        ax_recall.set_xticklabels([])
        ax_recall.grid(True, linestyle='--', alpha=0.3)

        # --- Plot Precision ---
        if precision_col in df_precision.columns:
            ax_precision.plot(x_labels, df_precision[precision_col], marker='o', linestyle=':', color='#1100ff', label="FastMultRec (1 WGD)")

        if lca_precision_col in df_precision.columns:
            ax_precision.plot(x_labels, df_precision[lca_precision_col], marker='s', linestyle='-', color='#ff000e', label="LCA (1 WGD)")

        ax_precision.set_ylim(0, 1.02)
        ax_precision.set_xlabel("D & L Rate", fontsize=20)
        if idx == 0:
            ax_precision.set_ylabel("Precision", fontsize=20)
        else:
            ax_precision.set_ylabel("")
        ax_precision.set_xticks(range(len(x_labels)))
        ax_precision.set_xticklabels(x_labels, rotation=90)
        ax_precision.grid(True, linestyle='--', alpha=0.3)

    # Add title and legend to figure
    #title_str = f"{'Cleaned constructed' if inferred else 'True'} gene trees with dup cost {dup_cost}"
    #fig.suptitle(title_str, fontsize=26)

    # Add shared legend below the plot
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=2, fontsize=18)
    fig.tight_layout(rect=[0, 0.05, 1, 0.93])  # leave space for suptitle and legend

if __name__ == "__main__":
    os.makedirs("plots", exist_ok=True)
    output_pdf_path = os.path.join("plots", "all_recall_precision_costs.pdf")
    
    with PdfPages(output_pdf_path) as pdf:
        for cost in dup_costs:
            # Inferred trees
            fig = plt.figure(figsize=(20, 12))
            plot_page(fig, cost, recall_files_inferred, precision_files_inferred, inferred=True)
            pdf.savefig(fig)
            plt.close(fig)

            # True trees
            fig = plt.figure(figsize=(20, 12))
            plot_page(fig, cost, recall_files_true, precision_files_true, inferred=False)
            pdf.savefig(fig)
            plt.close(fig)

    print(f"All plots saved to: {output_pdf_path}")
