import os
import sys
import pandas as pd

# Function to calculate accuracy
def calculate_accuracy(reference, target, threshold=0.8):
    # Ensure both dataframes have the same index
    reference = reference.set_index(reference.columns[0])
    target = target.set_index(target.columns[0])
    
    # Filter species with Gis > 10 in target
    mask = target['Num Gis'] > 50
    filtered_target = target[mask]
    
    # Reindex the target DataFrame to ensure identical indexing
    filtered_reference = reference.reindex(filtered_target.index)
    
    # Calculate the difference
    difference = filtered_target['Num Gis'] - filtered_reference['Num Gis']
    
    # Count the species where the reference is greater than the target and the difference is within the threshold,
    # or where the reference is equal to or smaller than the target
    accuracy = sum((filtered_target['Num Gis'] > filtered_reference['Num Gis']) & 
                   (difference.abs() / filtered_target['Num Gis'] > 1 - threshold)) 
    
    # Calculate the accuracy percentage
    total_count = len(filtered_target)
    if total_count > 0:
        accuracy_percentage = (accuracy / total_count) * 100
    else:
        accuracy_percentage = 0
        
    return accuracy_percentage

# Function to process a single subdirectory
def process_subdir(subdir):
    # List of i values
    i_values = [5, 100]
    
    results = {'sim_number': os.path.basename(subdir)}
    
    # Load the simphy data
    simphy_file = os.path.join(subdir, 'out_simphy.txt.csv')
    if not os.path.exists(simphy_file):
        return None
    simphy_data = pd.read_csv(simphy_file)
    
    # Calculate accuracy for lca
    lca_file = os.path.join(subdir, 'out_lca.txt.csv')
    if os.path.exists(lca_file):
        lca_data = pd.read_csv(lca_file)
        results['lca_accuracy'] = calculate_accuracy(simphy_data, lca_data)
    
    # Calculate accuracy for greedy and greedy down algorithms
    for i in i_values:
        for algorithm in ['greedy', 'greedydown', 'stochastic']:
            variable_file = os.path.join(subdir, f'out_{algorithm}{i}.txt.csv')
            if os.path.exists(variable_file):
                variable_data = pd.read_csv(variable_file)
                results[f'{algorithm}{i}_accuracy'] = calculate_accuracy(simphy_data, variable_data)
    
    return results

# Main function to process all subdirectories and save the results as a CSV
def generate_csv(directory):
    os.chdir(directory)
    subdirs = [f"sim_{i}" for i in range(1, 101)]
    
    results = []
    for subdir in subdirs:
        if os.path.exists(subdir):
            result = process_subdir(subdir)
            if result:
                results.append(result)
    
    # Create a DataFrame and save it to a CSV file
    df = pd.DataFrame(results)
    output_file = f"{os.path.basename(directory)}-FP-WGD.csv"
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

# Usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    generate_csv(directory)
