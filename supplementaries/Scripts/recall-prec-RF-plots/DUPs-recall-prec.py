import os
import sys
import pandas as pd

# Function to calculate TP
def calculate_TP(reference, target, threshold=0.8):
    reference = reference.set_index(reference.columns[0])
    target = target.set_index(target.columns[0])
    mask = reference['Num Gis'] > 50
    filtered_reference = reference[mask]
    filtered_target = target.reindex(filtered_reference.index)
    difference = filtered_reference['Num Gis'] - filtered_target['Num Gis']
    TP = sum((filtered_reference['Num Gis'] > filtered_target['Num Gis']) & 
             (difference.abs() / filtered_reference['Num Gis'] <= 1 - threshold)) + \
         sum(filtered_reference['Num Gis'] <= filtered_target['Num Gis'])
    return TP

# Function to calculate FP
def calculate_FP(reference, target, threshold=0.8):
    reference = reference.set_index(reference.columns[0])
    target = target.set_index(target.columns[0])
    mask = target['Num Gis'] > 50
    filtered_target = target[mask]
    filtered_reference = reference.reindex(filtered_target.index)
    difference = filtered_target['Num Gis'] - filtered_reference['Num Gis']
    FP = sum((filtered_target['Num Gis'] > filtered_reference['Num Gis']) & 
             (difference.abs() / filtered_target['Num Gis'] > 1 - threshold))
    return FP

# Function to calculate FN
def calculate_FN(reference, target, threshold=0.8):
    reference = reference.set_index(reference.columns[0])
    target = target.set_index(target.columns[0])
    mask = reference['Num Gis'] > 50
    filtered_reference = reference[mask]
    filtered_target = target.reindex(filtered_reference.index)
    difference = filtered_reference['Num Gis'] - filtered_target['Num Gis']
    TP = sum((filtered_reference['Num Gis'] > filtered_target['Num Gis']) & 
             (difference.abs() / filtered_reference['Num Gis'] <= 1 - threshold)) + \
         sum(filtered_reference['Num Gis'] <= filtered_target['Num Gis'])
    total_count = len(filtered_reference)
    FN = total_count - TP
    return FN

# Function to process a single subdirectory
def process_subdir(subdir):
    i_values = [5, 100]
    results = {'sim_number': os.path.basename(subdir)}
    
    simphy_file = os.path.join(subdir, 'out_simphy.txt.csv')
    if not os.path.exists(simphy_file):
        return None
    simphy_data = pd.read_csv(simphy_file)
    
    for algorithm in ['lca'] + [f'{alg}{i}' for alg in ['greedy', 'greedydown', 'stochastic'] for i in i_values]:
        variable_file = os.path.join(subdir, f'out_{algorithm}.txt.csv')
        if os.path.exists(variable_file):
            variable_data = pd.read_csv(variable_file)
            TP = calculate_TP(simphy_data, variable_data)
            FP = calculate_FP(simphy_data, variable_data)
            FN = calculate_FN(simphy_data, variable_data)
            recall = TP / (TP + FN) if (TP + FN) > 0 else 0
            precision = TP / (TP + FP) if (TP + FP) > 0 else 0
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
        output_file = f"{os.path.basename(directory)}-{metric}-WGD.csv"
        metric_df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")

# Usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    generate_csv(directory)
