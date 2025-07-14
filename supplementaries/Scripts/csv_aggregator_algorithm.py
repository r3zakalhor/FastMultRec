import os
import glob
import csv
import argparse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D

# Define the mapping for Duprate substrings to legend strings
DU_RATE_LEGENDS = {
    'Duprate-18': 'D&L Rate = F:1e-18',
    'Duprate-15': 'D&L Rate = F:1e-15',
    'Duprate-11': 'D&L Rate = F:1e-11',
    'Duprate-10': 'D&L Rate = F:1e-10',
    'Duprate-9': 'D&L Rate = F:1e-9',
    'Duprate-8': 'D&L Rate = F:1e-8',
    'Duprate-7': 'D&L Rate = F:1e-7',
    'Duprate-6': 'D&L Rate = F:1e-6',
    'Duprate_u-gb_0.1': 'D&L Rate = LN:(U:-25,-15),0.1',
    'Duprate_u-gb_0.3': 'D&L Rate = LN:(U:-25,-15),0.3',
    'Duprate_u-gb_1': 'D&L Rate = LN:(U:-25,-15),1',
    'Duprate_u-6_-12': 'D&L Rate = U:1e-6,1e-12'
}

def draw_bar_chart(all_data, title, xlabel, ylabel, bar_names):
    fig, ax = plt.subplots(figsize=(16, 10))  # Increase the figure size
    num_directories = len(all_data)
    num_bars = len(bar_names)
    bar_width = 0.25  # Width of each bar, adjusted for 3 bars

    x = []
    heights = []
    colors = []
    labels = list(all_data.keys())

    for i, (dir_name, data) in enumerate(all_data.items()):
        for j in range(num_bars):
            x.append(i * (num_bars + 1) + j * bar_width)  # Position of each bar
            if j < len(data):
                heights.append(data[j][1])
                if j == 0:
                    colors.append('b')
                elif j == 1:
                    colors.append('g')
                elif j == 2:
                    colors.append('r')
            else:
                heights.append(0)
                if j == 0:
                    colors.append('b')
                elif j == 1:
                    colors.append('g')
                else:
                    colors.append('r')

    ax.bar(x, heights, bar_width, color=colors)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Modify x-axis labels based on DU_RATE_LEGENDS
    x_labels = []
    for label in labels:
        label = str(label)  # Ensure the label is a string
        pos = label.find("Duprate")
        if pos != -1:
            label = label[pos:]
        custom_label = DU_RATE_LEGENDS.get(label, label)
        x_labels.append(custom_label)

    ax.set_xticks([i * (num_bars + 1) + bar_width * (num_bars / 2) for i in range(num_directories)])
    ax.set_xticklabels(x_labels)
    plt.xticks(rotation=50, ha='right')

    # Add legend
    legend_elements = [Line2D([0], [0], color='b', lw=4, label=bar_names[0]),
                       Line2D([0], [0], color='g', lw=4, label=bar_names[1]),
                       Line2D([0], [0], color='r', lw=4, label=bar_names[2])]
    ax.legend(handles=legend_elements, loc='upper right')

    # Ensure both positive and negative values are visible on y-axis
    ax.axhline(y=0, color='black', linewidth=0.5)  # Add horizontal line at y=0

    # Adjust y-axis limits to ensure visibility of both positive and negative values
    min_value = min(min(heights), 0) * 1.1  # Expand by 10% to ensure visibility
    max_value = max(max(heights), 0) * 1.1
    ax.set_ylim(min_value, max_value)

    plt.tight_layout()
    return fig

def calculate_sum_from_csv(file_path, col_index):
    total = 0
    count = 0
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row if there is one
        for row in reader:
            try:
                value = float(row[col_index])
                total += value
                count += 1
            except ValueError:
                print(f"Non-numeric value found in file {file_path}, row {row}")
    return total if count > 0 else float('nan')

def calculate_average_improvement_from_csv(file_path, col_index1, col_index2):
    total = 0
    count = 0
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row if there is one
        for row in reader:
            try:
                value1 = float(row[col_index1])
                if value1 > 0:
                    value2 = float(row[col_index2])
                    total += (1 - value2 / value1)
                    count += 1
            except ValueError:
                print(f"Non-numeric value found in file {file_path}, row {row}")
    return total / count if count > 0 else float('nan')

def get_dl_cost_from_filename(filename):
    pz = filename.split("_")
    for i in range(len(pz)):
        if i > 0 and pz[i][0] == "l" and pz[i - 1][0] == "d":
            return pz[i - 1]
    return 0

def process_directory(directory, csv_files):
    dist_sums = []
    improv_avgs = []
    cost_sums = []
    pct_improv = []

    for file in csv_files:
        file_path = os.path.join(directory, file)
        if os.path.exists(file_path):
            print(f"Processing file: {file_path}")
            
            if len(dist_sums) == 0:
                lcasum = calculate_sum_from_csv(file_path, col_index=0)
                dist_sums.append(("lcamap", lcasum))
                improv_avgs.append(("lcamap", 0))

            dlcost_str = get_dl_cost_from_filename(file)

            grsum = calculate_sum_from_csv(file_path, col_index=1)
            dist_sums.append((dlcost_str, grsum))

            lcacostsum = calculate_sum_from_csv(file_path, col_index=8)
            cost_sums.append((dlcost_str + "lca", lcacostsum))

            grcostsum = calculate_sum_from_csv(file_path, col_index=11)
            cost_sums.append((dlcost_str + "gr", grcostsum))

            gr_improv_avg = calculate_average_improvement_from_csv(file_path, col_index1=0, col_index2=1)
            improv_avgs.append((dlcost_str, gr_improv_avg))

    # Replace 'd10' keys with directory names and calculate pct_improv
    lcamap_cost = dist_sums[0][1]
    pct_improv = [(key, 1 - d / lcamap_cost) for (key, d) in dist_sums]

    # Remove 'lcamap' entries
    dist_sums = [(key, value) for key, value in dist_sums if key != 'lcamap']
    improv_avgs = [(key, value) for key, value in improv_avgs if key != 'lcamap']
    pct_improv = [(key, value) for key, value in pct_improv if key != 'lcamap']

    # Ensure unique keys in cost_sums
    cost_sums = list(set(cost_sums))  # Convert to set to remove duplicates

    return dist_sums, improv_avgs, cost_sums, pct_improv

def main(directory_prefix, csv_files, bar_names):
    directories = glob.glob(f'{directory_prefix}*')

    all_dist_sums = {}
    all_improv_avgs = {}
    all_cost_sums = {}
    all_pct_improv = {}

    for directory in directories:
        if not os.path.isdir(directory):
            continue
        dir_name = os.path.basename(directory)
        dist_sums, improv_avgs, cost_sums, pct_improv = process_directory(directory, csv_files)
        
        all_dist_sums[dir_name] = dist_sums[:3]  # Ensure only three bars per directory
        all_improv_avgs[dir_name] = improv_avgs[:3]
        all_cost_sums[dir_name] = cost_sums[:3]
        all_pct_improv[dir_name] = pct_improv[:3]

    with PdfPages('combined_results.pdf') as pdf:
        fig = draw_bar_chart(all_dist_sums, "Total path distance error vs simulated, sum of all datasets", "Directories", "Ttl path dist error", bar_names)
        #pdf.savefig(fig)
        #plt.close(fig)

        fig = draw_bar_chart(all_cost_sums, "Total reconciliation cost, sum of all datasets", "Directories", "Ttl cost", bar_names)
        #pdf.savefig(fig)
        #plt.close(fig)

        #fig = draw_bar_chart(all_pct_improv, "Improvement % of path dist over final total", "Directories", "Ttl %", bar_names)
        fig = draw_bar_chart(all_pct_improv, "", "D & L Rate", "Improvement (%)", bar_names)
        pdf.savefig(fig)
        plt.close(fig)

        fig = draw_bar_chart(all_improv_avgs, "", "D & L Rate", "Improvement (%)", bar_names)
        #pdf.savefig(fig)
        #plt.close(fig)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize CSV data across directories.")
    parser.add_argument('directory_prefix', type=str, help='The prefix for directories containing the CSV files')
    parser.add_argument('csv_files', type=str, nargs=3, help='The three CSV files to be processed')
    parser.add_argument('bar_names', type=str, nargs=3, help='The names for the bars in the plot')

    args = parser.parse_args()
    main(args.directory_prefix, args.csv_files, args.bar_names)