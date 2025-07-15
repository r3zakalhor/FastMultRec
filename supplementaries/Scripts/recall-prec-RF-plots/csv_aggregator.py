import os
import glob
import csv
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

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

def get_num_species(directory):
    newick_file = os.path.join(directory, 'source_s_tree.trees')
    if not os.path.exists(newick_file):
        print(f"Error: File not found: {newick_file}")
        return None  # Handle this case appropriately

    with open(newick_file, 'r') as f:
        content = f.read()
        # Example logic to count nodes in the Newick tree
        num_species = content.count('(')
    return num_species

def process_first_csv(directory, prefix):
    csv_files = glob.glob(os.path.join(directory, f'{prefix}*.csv'))

    if not csv_files:
        print(f"No CSV files found in directory: {directory}")
        return None

    first_csv_file = csv_files[0]
    results = []

    with open(first_csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row if there is one
        for row in reader:
            try:
                lca = float(row[0])  # Column 1 (index 0)
                greedy = float(row[1])  # Column 2 (index 1)
                dup_height = float(row[6])  # Column 7 (index 6)
                sim_directory = os.path.join(directory, f'sim_{reader.line_num - 1}')  # Use line number as simulation number
                num_species = get_num_species(sim_directory)

                if num_species is not None:
                    results.append({
                        'LCA': lca,
                        'Greedy': greedy,
                        'Dup Height': dup_height,
                        'Num Species': num_species
                    })
            except ValueError:
                print(f"Non-numeric value found in CSV file {first_csv_file}, row {reader.line_num}")

    return results

def main(directory_pattern, prefix):
    directories = glob.glob(directory_pattern)

    all_results = []

    for directory in directories:
        if not os.path.isdir(directory):
            continue
        results = process_first_csv(directory, prefix)
        if results:
            all_results.extend(results)

    lca_values = [result['LCA'] for result in all_results]
    greedy_values = [result['Greedy'] for result in all_results]
    dup_heights = [result['Dup Height'] for result in all_results]
    num_species = [result['Num Species'] for result in all_results]
    simulation_numbers = np.arange(1, len(all_results) + 1)

    df = pd.DataFrame({
        'simulation': simulation_numbers,
        'lca': lca_values,
        'greedy': greedy_values,
        'dup_height': dup_heights,
        'num_species': num_species
    })

    # Create a figure with two subplots (one on top of the other)
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 16))

    # Plotting the violin plot on the first subplot
    sns.violinplot(x='simulation', y='dup_height', data=df, palette='viridis', linewidth=2.5, ax=axes[0])

    # Adding median line to the violin plot
    median_dup_heights = df.groupby('simulation')['dup_height'].median().values
    axes[0].plot(np.arange(len(median_dup_heights)), median_dup_heights, marker='o', color=(1.0, 0.5, 0.5, 0.8), label='Median Dup Height')

    # Add annotations for number of species
    for i, group in enumerate(df.groupby('simulation')):
        sim_number, data = group
        for j, row in data.iterrows():
            species_color = sns.color_palette('viridis', as_cmap=True)(row['num_species'] / 100.0)
            axes[0].text(i, row['dup_height'], str(row['num_species']),
                         horizontalalignment='center', verticalalignment='bottom',
                         fontsize=8, color=species_color, weight='bold')

    # Custom legend for number of species
    handles = [plt.Line2D([0], [0], color=sns.color_palette('viridis', as_cmap=True)(i / 100.0), lw=4) for i in range(0, 101, 20)]
    labels = [str(i) for i in range(0, 101, 20)]
    axes[0].legend(handles, labels, title='Number of Species')

    # Setting the title for the violin plot
    directory_name = os.path.basename(directory_pattern.rstrip('/'))
    axes[0].set_title(f"Violin Plot for '{directory_name}'")
    axes[0].set_xlabel('Simulation Number')
    axes[0].set_ylabel('Dup Height')

    # Adjusting x-axis tick positions and labels
    axes[0].set_xticks(np.arange(0, len(simulation_numbers), 5))
    axes[0].set_xticklabels(simulation_numbers[np.arange(0, len(simulation_numbers), 5)])

    # Plotting the linear plot for improvement percentage on the second subplot
    improvement = 1 - (df['greedy'] / df['lca'])
    axes[1].plot(df['simulation'], improvement, marker='o', color='blue')

    # Adding a horizontal line at y=0
    axes[1].axhline(0, color='red', linestyle='--')

    # Setting the title and labels for the second plot
    axes[1].set_title('Improvement %')
    axes[1].set_xlabel('Simulation Number')
    axes[1].set_ylabel('%')
    axes[1].legend()

    plt.tight_layout()

    # Save the combined plot as a single PDF
    plt.savefig('combined_plot.pdf')
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process first CSV file in some directories.')
    parser.add_argument('directory_pattern', type=str, help='Directory pattern to process')
    parser.add_argument('--prefix', type=str, default='', help='Prefix for CSV files')
    args = parser.parse_args()
    main(args.directory_pattern, args.prefix)
