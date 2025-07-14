import os
import sys
import pandas as pd

def calculate_metrics(reference, target, t1, t2, total_gene_trees, use_app=True):
    reference = reference.set_index(reference.columns[0])
    target = target.set_index(target.columns[0])

    threshold1 = int(total_gene_trees * t1 / 100)
    threshold2 = int(total_gene_trees * t2 / 100)

    mask_reference = (reference['Num Gis'] >= threshold1) & (reference['Num Gis'] <= threshold2)
    mask_target = (target['Num Gis'] >= threshold1) & (target['Num Gis'] <= threshold2)

    if use_app:
        exclusion_mask = (2 * target['Num App'] >= target['Num Gis'])
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

    gene_tree_file = os.path.join(subdir, 'applied_loss_fix_all_genetrees_edited_scaledby_0.606479_h_cleaned_iqtree_rerooted_improvedTreesDL_ultrafastb1000_90_1.txt')
    if not os.path.exists(gene_tree_file):
        return None
    with open(gene_tree_file) as f:
        total_gene_trees = len(f.readlines()) - 1

    for t in [90]:
        for d in [1]:
            #algorithms = [f'out_greedydown{i}_improvedTreesDL_b1000_{t}_{d}' for i in [100]] + \
            #             [f'out_lca_improvedTreesDL_b1000_{t}_{d}']
            algorithms = [f'out_greedydown{i}_improvedTreesDL_b1000_unclean' for i in [100]] + [f'out_lca_improvedTreesDL_b1000_unclean']

            for algorithm in algorithms:
                variable_file = os.path.join(subdir, f'{algorithm}.txt.csv')
                if os.path.exists(variable_file):
                    variable_data = pd.read_csv(variable_file)
                    TP, FP, FN = calculate_metrics(simphy_data, variable_data, t1, t2, total_gene_trees, use_app=False)
                    recall = TP / (TP + FN) if (TP + FN) > 0 else 'N/A'
                    precision = TP / (TP + FP) if (TP + FP) > 0 else 'N/A'
                    results[f'{algorithm}_TP'] = TP
                    results[f'{algorithm}_FP'] = FP
                    results[f'{algorithm}_FN'] = FN
                    results[f'{algorithm}_recall'] = recall
                    results[f'{algorithm}_precision'] = precision

    # --- Handle MetaEc_out.csv separately ---
    metaec_file = os.path.join(subdir, 'MetaEc_out_uncleaned.csv')
    if os.path.exists(metaec_file):
        metaec_data = pd.read_csv(metaec_file)
        TP, FP, FN = calculate_metrics(simphy_data, metaec_data, t1, t2, total_gene_trees, use_app=False)
        recall = TP / (TP + FN) if (TP + FN) > 0 else 'N/A'
        precision = TP / (TP + FP) if (TP + FP) > 0 else 'N/A'
        results['MetaEc_out_TP'] = TP
        results['MetaEc_out_FP'] = FP
        results['MetaEc_out_FN'] = FN
        results['MetaEc_out_recall'] = recall
        results['MetaEc_out_precision'] = precision

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
    #algorithms = [f'out_greedydown{i}_improvedTreesDL_b1000_{t}_{d}' for i in [100] for t in [90] for d in [1]] + \
    #             [f'out_lca_improvedTreesDL_b1000_{t}_{d}' for t in [90] for d in [1]] + ['MetaEc_out']
    algorithms = [f'out_greedydown{i}_improvedTreesDL_b1000_unclean' for i in [100] for t in [90] for d in [1]] + [f'out_lca_improvedTreesDL_b1000_unclean' for t in [90] for d in [1]] + ['MetaEc_out']

    for metric in metrics:
        metric_cols = ['sim_number'] + [f'{algorithm}_{metric}' for algorithm in algorithms if f'{algorithm}_{metric}' in df.columns]
        metric_df = df[metric_cols]
        #output_file = f"{os.path.basename(directory)}-{metric}-1W-WGD-improvedtrees-bootstrap-b1000-2NumApp-t{int(t1)}-t{int(t2)}.csv"
        output_file = f"{os.path.basename(directory)}-{metric}-1W-WGD-unclean-2NumApp-t{int(t1)}-t{int(t2)}.csv"
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
