import os
import sys
import pandas as pd

# Function to calculate TP, FP, and FN
def calculate_metrics(reference, target, t1, t2):
    reference = reference.set_index(reference.columns[0])
    target = target.set_index(target.columns[0])
    
    mask_reference = (reference['Num Gis'] >= t1) & (reference['Num Gis'] <= t2)
    mask_target = (target['Num Gis'] >= t1) & (target['Num Gis'] <= t2)
    
    filtered_reference = reference[mask_reference]
    filtered_target = target.reindex(filtered_reference.index)
    
    TP = sum(mask_reference & mask_target)
    FP = sum(~mask_reference & mask_target)
    FN = sum(mask_reference & ~mask_target)
    
    return TP, FP, FN

# Function to process a single subdirectory
def process_subdir(subdir, t1, t2):
    i_values = [3, 10, 50, 100]
    results = {'sim_number': os.path.basename(subdir)}
    
    simphy_file = os.path.join(subdir, 'out_simphy.txt.csv')
    if not os.path.exists(simphy_file):
        return None
    simphy_data = pd.read_csv(simphy_file)
    
    #for algorithm in ['lca'] + [f'{alg}{i}' for alg in ['greedy', 'greedydown', 'stochastic'] for i in i_values]:
    for algorithm in ['lca'] + [f'{alg}{i}' for alg in ['greedydown'] for i in i_values]:
        variable_file = os.path.join(subdir, f'out_{algorithm}.txt.csv')
        if os.path.exists(variable_file):
            variable_data = pd.read_csv(variable_file)
            TP, FP, FN = calculate_metrics(simphy_data, variable_data, t1, t2)
            recall = TP / (TP + FN) if (TP + FN) > 0 else 'N/A'
            precision = TP / (TP + FP) if (TP + FP) > 0 else 'N/A'
            results[f'{algorithm}_TP'] = TP
            results[f'{algorithm}_FP'] = FP
            results[f'{algorithm}_FN'] = FN
            results[f'{algorithm}_recall'] = recall
            results[f'{algorithm}_precision'] = precision
    
    return results

# Main function to process all subdirectories and save the results as CSV
def generate_csv(directory, t1, t2):
    os.chdir(directory)
    subdirs = [f"sim_{i}" for i in range(1, 26)]
    
    results = []
    for subdir in subdirs:
        if os.path.exists(subdir):
            result = process_subdir(subdir, t1, t2)
            if result:
                results.append(result)
    
    df = pd.DataFrame(results)
    
    metrics = ['TP', 'FP', 'FN', 'recall', 'precision']
    #algorithms = ['lca'] + [f'{alg}{i}' for alg in ['greedy', 'greedydown', 'stochastic'] for i in [5, 100]]
    algorithms = ['lca'] + [f'{alg}{i}' for alg in ['greedydown'] for i in [3, 10, 50, 100]]
    
    for metric in metrics:
        metric_df = df[['sim_number'] + [f'{algorithm}_{metric}' for algorithm in algorithms]]
        output_file = f"{os.path.basename(directory)}-{metric}-0W-SD-t20-t80.csv"
        metric_df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")

# Usage
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <directory> <threshold1> <threshold2>")
        sys.exit(1)
    
    directory = sys.argv[1]
    t1 = float(sys.argv[2])
    t2 = float(sys.argv[3])
    generate_csv(directory, t1, t2)
