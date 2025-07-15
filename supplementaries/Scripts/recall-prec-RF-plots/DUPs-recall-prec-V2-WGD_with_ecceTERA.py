import os
import sys
import pandas as pd

def calculate_metrics(reference, target, t1, t2, total_gene_trees):
    reference = reference.set_index(reference.columns[0])
    target = target.set_index(target.columns[0])
    
    # Calculate thresholds as percentages of total gene trees
    threshold1 = int(total_gene_trees * t1 / 100)
    threshold2 = int(total_gene_trees * t2 / 100)
    
    # Apply masks based on threshold
    mask_reference = (reference['Num Gis'] >= threshold1) & (reference['Num Gis'] <= threshold2)
    mask_target = (target['Num Gis'] >= threshold1) & (target['Num Gis'] <= threshold2)

    # Exclude rows where 2 * Num App < Num Gis in the target file
    exclusion_mask = (2 * target['Num App'] >= target['Num Gis'])

    # Apply the exclusion condition to both masks
    mask_reference = mask_reference & exclusion_mask
    mask_target = mask_target & exclusion_mask    


    TP = sum(mask_reference & mask_target)
    FP = sum(~mask_reference & mask_target)
    FN = sum(mask_reference & ~mask_target)
    
    return TP, FP, FN

def process_subdir(subdir, t1, t2):
    results = {'sim_number': os.path.basename(subdir)}
    
    simphy_file = os.path.join(subdir, 'out_simphy.txt.csv')
    if not os.path.exists(simphy_file):
        return None
    simphy_data = pd.read_csv(simphy_file)
    
    # Read the gene tree file to get the total number of gene trees
    gene_tree_file = os.path.join(subdir, 'applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree_rerooted_improvedTreesDL_ultrafastb1000_90_1.txt')
    if not os.path.exists(gene_tree_file):
        return None
    with open(gene_tree_file) as f:
        total_gene_trees = len(f.readlines()) - 1 # Number of gene trees is the number of lines in the file
    
    for t in [90]:  # You can adjust this as per your need
        for d in [1]:
            for algorithm in [f'out_greedydown{i}_improvedTreesDL_b1000_{t}_{d}' for i in [3, 10, 50, 60, 70, 80, 90, 100]] + [f'out_lca_improvedTreesDL_b1000_{t}_{d}']:
            #for algorithm in [f'out_true_greedydown{i}' for i in [3, 10, 50, 60, 70, 80, 90, 100]] + [f'out_true_lca']:
            #for algorithm in [f'out_greedydown{i}_improvedTreesDL_b1000_unclean' for i in [3, 10, 50, 60, 70, 80, 90, 100]] + [f'out_lca_improvedTreesDL_b1000_unclean']:
                variable_file = os.path.join(subdir, f'{algorithm}.txt.csv')
                if os.path.exists(variable_file):
                    variable_data = pd.read_csv(variable_file)
                    TP, FP, FN = calculate_metrics(simphy_data, variable_data, t1, t2, total_gene_trees)
                    recall = TP / (TP + FN) if (TP + FN) > 0 else 'N/A'
                    precision = TP / (TP + FP) if (TP + FP) > 0 else 'N/A'
                    results[f'{algorithm}_TP'] = TP
                    results[f'{algorithm}_FP'] = FP
                    results[f'{algorithm}_FN'] = FN
                    results[f'{algorithm}_recall'] = recall
                    results[f'{algorithm}_precision'] = precision
    
    return results

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
    algorithms = [f'out_greedydown{i}_improvedTreesDL_b1000_{t}_{d}' for i in [3, 10, 50, 60, 70, 80, 90, 100] for t in [90] for d in [1]] + [f'out_lca_improvedTreesDL_b1000_{t}_{d}' for t in [90] for d in [1]]
    #algorithms = [f'out_true_greedydown{i}' for i in [3, 10, 50, 60, 70, 80, 90, 100] for t in [90] for d in [1]] + [f'out_true_lca' for t in [90] for d in [1]]
      
    for metric in metrics:
        metric_df = df[['sim_number'] + [f'{algorithm}_{metric}' for algorithm in algorithms if f'{algorithm}_{metric}' in df.columns]]
        output_file = f"{os.path.basename(directory)}-{metric}-2W-WGD-improvedtrees-bootstrap-b1000-2NumApp-t{int(t1)}-t{int(t2)}.csv"
        #output_file = f"{os.path.basename(directory)}-{metric}-2W-WGD-true-t{int(t1)}-t{int(t2)}.csv"
        metric_df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <directory> <threshold1> <threshold2>")
        sys.exit(1)
    
    directory = sys.argv[1]
    t1 = float(sys.argv[2])
    t2 = float(sys.argv[3])
    generate_csv(directory, t1, t2)
