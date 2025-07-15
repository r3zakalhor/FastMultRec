import os
import glob
import csv
import argparse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import re

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

def draw_bar_chart(data, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(16, 10))  # Increase the figure size
    num_directories = len(data)
    bar_width = 0.8 / num_directories  # Adjust the bar width to reduce overlap
    space_between_groups = 0.2  # Space between groups of bars

    for i, (label, values) in enumerate(data.items()):
        x_values = list(range(len(values)))
        y_values = [y * 100 for x, y in values]  # Multiply y-values by 100
        # Use the custom legend string
        pos = label.find("Duprate")
        label = label[pos:]
        custom_label = DU_RATE_LEGENDS.get(label, label)
        ax.bar([x + i * bar_width for x in x_values], y_values, bar_width, label=custom_label)

    # Increase font sizes
    ax.set_title(title, fontsize=20)  # Increase title font size
    ax.set_xlabel(xlabel, fontsize=18)  # Increase x-axis label font size
    ax.set_ylabel(ylabel, fontsize=18)  # Increase y-axis label font size
    ax.legend(fontsize=18)  # Increase legend font size
    ax.set_xticks([r + bar_width * (num_directories - 1) / 2 for r in x_values])
    ax.set_xticklabels([x.replace('d', '') for x, y in values], fontsize=18)  # Increase x-axis tick labels size
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=18)  # Increase y-axis tick labels size

    # Adjust legend to be horizontal inside the plot, at the top
    ax.legend(fontsize=16, loc='upper center', bbox_to_anchor=(0.37, 1),
              ncol=3, frameon=False)
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
    if (total == 0 and col_index == 0):
         print("LCASum is 0 in ", file_path)
    return total if count > 0 else float('nan')

def calculate_average_improvement_from_csv(file_path, col_index1, col_index2):
    total = 0
    count = 0
    count00 = 0
    count01 = 0 

    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row if there is one
        for row in reader:
            try:
                value1 = float(row[col_index1])
                value2 = float(row[col_index2])
                if value1 == 0  and value2 !=0:
                    count01 += 1
                if value1 == 0  and value2 ==0:
                    count00 += 1
                if value1 > 0:
                    total += (1 - value2 / value1)
                    count += 1
            except ValueError:
                print(f"Non-numeric value found in file {file_path}, row {row}")
    return total / count if count > 0 else float('nan'), count01, count00

def get_dl_cost_from_filename(filename):
    pz = filename.split("_")
    for i in range(len(pz)):
        if i > 0 and pz[i][0] == "l" and pz[i - 1][0] == "d":
            return pz[i - 1]
    return 0

def extract_duprate_value(directory_name):
    match = re.search(r'Duprate-([\d.]+)', directory_name)
    return float(match.group(1)) if match else -1  # Assign -1 if no match is found

def process_directory(directory, prefix):
    # Define the specific numbers for X
    #X_values = {2, 5, 30, 100}
    X_values = {2, 3, 4, 5, 10, 20, 30, 50, 70, 100}
    # Use glob to get all files that match the broad pattern
    csv_files = glob.glob(os.path.join(directory, f'{prefix}*.csv'))
    # Create a regular expression pattern to match _dX_ where X is in {2, 5, 30, 100}
    pattern = re.compile(rf'_d({"|".join(map(str, X_values))})_')
    #csv_files = glob.glob(os.path.join(directory, f'{prefix}*.csv'))
    sumcount00 = 0
    sumcount01 = 0 

    dist_sums = []
    improv_avgs = []
    cost_sums = []
    filtered_csv_files = [f for f in csv_files if pattern.search(f)]
    #for file in csv_files:
    for file in filtered_csv_files:
        if len(dist_sums) == 0:
            lcasum = calculate_sum_from_csv(file, col_index=0)
            dist_sums.append(("LCA", lcasum))
            improv_avgs.append(("LCA", 0))

        dlcost_str = get_dl_cost_from_filename(file)

        grsum = calculate_sum_from_csv(file, col_index=1)
        dist_sums.append((dlcost_str, grsum))

        lcacostsum = calculate_sum_from_csv(file, col_index=8)
        cost_sums.append((dlcost_str + "lca", lcacostsum))

        grcostsum = calculate_sum_from_csv(file, col_index=11)
        cost_sums.append((dlcost_str + "gr", grcostsum))

        gr_improv_avg, count01, count00 = calculate_average_improvement_from_csv(file, col_index1=0, col_index2=1)
        sumcount01 += count01
        sumcount00 += count00
        improv_avgs.append((dlcost_str, gr_improv_avg))

    dist_sums.sort(
        key=lambda s: (0 if s[0] == "LCA" else float(s[0].replace("d", ""))))
    improv_avgs.sort(
        key=lambda s: (0 if s[0] == "LCA" else float(s[0].replace("d", ""))))
    cost_sums.sort(key=lambda s: (
        float(s[0].replace("d", "").replace("lca", "").replace("gr", ""))))

    lcamap_cost = dist_sums[0][1]

    if lcamap_cost != 0:
        pct_improv = [(key, 1 - d / lcamap_cost) for (key, d) in dist_sums]
    else:
        #print(f"Warning: lcamap_cost is zero for directory {directory}. Setting improvement to NaN.")
        pct_improv = [(key, float('nan')) for (key, d) in dist_sums]
    print(directory)
    #print("lcs dist is 0 but greedy is not: ", sumcount01)
    #print("lcs dist is 0 but greedy is 0: ", sumcount00)
    return dist_sums, improv_avgs, cost_sums, pct_improv

def main(directory_pattern, prefix):
    directories = glob.glob(directory_pattern)

    # Extract duprate values and sort, ensuring those with -1 are placed at the end
    dir_duprates = [(os.path.basename(directory), extract_duprate_value(directory)) for directory in directories]
    dir_duprates.sort(key=lambda x: x[1], reverse=True)  # Sort in decreasing order

    all_dist_sums = {}
    all_improv_avgs = {}
    all_cost_sums = {}
    all_pct_improv = {}

    for dir_name, _ in dir_duprates:
        directory = os.path.join(os.path.dirname(directory_pattern), dir_name)
        if not os.path.isdir(directory):
            continue
        dist_sums, improv_avgs, cost_sums, pct_improv = process_directory(directory, prefix)
        all_dist_sums[dir_name] = dist_sums
        all_improv_avgs[dir_name] = [item for item in improv_avgs if item[0] != "LCA"]
        all_cost_sums[dir_name] = cost_sums
        all_pct_improv[dir_name] = [item for item in pct_improv if item[0] != "LCA"]

    with PdfPages('combined_results.pdf') as pdf:
        fig = draw_bar_chart(all_dist_sums, "", "Duplication cost", "Total path distances error")
        pdf.savefig(fig)
        plt.close(fig)

        fig = draw_bar_chart(all_cost_sums, "Total reconciliation cost, sum of all datasets", "Method", "Ttl cost")
        #pdf.savefig(fig)
        #plt.close(fig)

        #fig = draw_bar_chart(all_pct_improv, "Improvement % of path dist over final total", "Method", "Ttl %")
        fig = draw_bar_chart(all_pct_improv, "", "Duplication cost", "Improvement (%)")
        pdf.savefig(fig)
        plt.close(fig)

        fig = draw_bar_chart(all_improv_avgs, "", "Duplication cost", "Improvement (%)")
        #pdf.savefig(fig)
        #plt.close(fig)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate the average of the second column of all CSV files in a directory.")
    parser.add_argument('directory_pattern', type=str, help='The pattern for directories containing the CSV files (e.g., WGD*)')
    parser.add_argument('prefix', type=str, help='The prefix of the CSV files')

    args = parser.parse_args()
    main(args.directory_pattern, args.prefix)