import os
import sys
import pandas as pd
import re

# Function to extract trees from the file and calculate TP, FP, and FN
def calculate_metrics(file_path):
    def parse_trees(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        trees = re.findall(r'<GENETREES>(.*?)</GENETREES>', content, re.DOTALL)
        trees = trees[0].strip().split('\n') if trees else []
        return trees

    def count_labels(tree):
        TP, FP, FN = 0, 0, 0
        internal_nodes = re.findall(r'\)([^,;\(\)]+)(?=[\),;])', tree)
        for node in internal_nodes:
            # print(node)
            parts = node.split('_')
            if len(parts) >= 5:  # Ensure there are enough parts to analyze
                if (parts[2] == 'Dup' or parts[2] == 'Dup:0') and parts[4] == 'Dup':
                    if parts[1] == parts[3]:
                        TP += 1
                    else:
                        FN += 1
                elif (parts[2] == 'Dup' or parts[2] == 'Dup:0'):
                    FN += 1
                elif parts[4] == 'Dup':
                    FP += 1
        return TP, FP, FN

    trees = parse_trees(file_path)
    total_TP, total_FP, total_FN = 0, 0, 0
    for tree in trees:
        TP, FP, FN = count_labels(tree)
        total_TP += TP
        total_FP += FP
        total_FN += FN

    return total_TP, total_FP, total_FN

# Function to process a single subdirectory
def process_subdir(subdir):
    i_values = [5, 100]
    results = {'sim_number': os.path.basename(subdir)}

    for algorithm in ['lca'] + [f'{alg}{i}' for alg in ['greedy', 'greedydown', 'stochastic'] for i in i_values]:
        variable_file = os.path.join(subdir, f'out_{algorithm}.txt')
        if os.path.exists(variable_file):
            TP, FP, FN = calculate_metrics(variable_file)
            recall = TP / (TP + FN) if (TP + FN) > 0 else 'N/A'
            precision = TP / (TP + FP) if (TP + FP) > 0 else 'N/A'
            results[f'{algorithm}_TP'] = TP
            results[f'{algorithm}_FP'] = FP
            results[f'{algorithm}_FN'] = FN
            results[f'{algorithm}_recall'] = recall
            results[f'{algorithm}_precision'] = precision

    return results

# Main function to process all subdirectories and save the results as CSV
def generate_csv(directory):
    os.chdir(directory)
    subdirs = [f"sim_{i}" for i in range(1, 101)]

    results = []
    for subdir in subdirs:
        if os.path.exists(subdir):
            result = process_subdir(subdir)
            if result:
                results.append(result)

    df = pd.DataFrame(results)

    metrics = ['TP', 'FP', 'FN', 'recall', 'precision']
    algorithms = ['lca'] + [f'{alg}{i}' for alg in ['greedy', 'greedydown', 'stochastic'] for i in [5, 100]]

    for metric in metrics:
        metric_df = df[['sim_number'] + [f'{algorithm}_{metric}' for algorithm in algorithms]]
        output_file = f"{os.path.basename(directory)}-{metric}-V3.csv"
        metric_df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")

# Usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    generate_csv(directory)
