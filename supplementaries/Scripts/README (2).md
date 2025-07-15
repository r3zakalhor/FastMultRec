# 🧪 Useful Scripts for Gene Tree Simulation and Analysis

This repository contains all supporting scripts used in our experiments, located under the `supplementaries/Scripts/` directory.

---

## 📁 Directory Structure

### `simulate_gene_trees/`

This directory includes all the scripts required to simulate **species trees** and **gene trees** using the [SimPhy](https://github.com/adamallo/SimPhy) framework.

#### 🔧 Main Script: `all_sim.py`

This script orchestrates the full simulation pipeline.

**Features:**
- Allows specifying the number of Whole Genome Duplications (WGD) to simulate:
  - `0`: no WGD
  - `1`: single WGD
  - `2`: double WGD
- Automatically applies **fractionation** (gene loss) on the duplicated gene trees.
- Generates output compatible with downstream phylogenomic reconciliation analysis.


### `generate_reconstructed_gene_trees/`

This section covers how to reconstruct gene trees from simulated sequences.

#### 🧬 Step 1: Convert gene trees to sequences

Use the `call_convert_genetrees_to_seq.py` script, which wraps around **Seq-Gen**, to simulate sequence evolution from gene trees.

#### 🧬 Step 2: Reconstruct gene trees from sequences

Use the `run_iqtree.sh` script to reconstruct gene trees using the [IQ-TREE](http://www.iqtree.org/) tool.


### `clean_constructed_gene_trees/`

After gene tree reconstruction, some gene trees may contain low-support or erroneous branches. To clean them:

#### 🧹 Script: `clean_genetrees_with_ecceTera.sh`

This script uses the **ecceTERA** tool to clean the reconstructed gene trees by reconciling them with a species tree and resolving low-confidence branches.



### `generate_FastmultRec_LCA_MetaEC_results/`

You can use the `analyze_sims_parallel_greedy_down.sh` or `run_metaec.py` scripts to generate results from **FastMultRec**, **LCA**, and **MetaEC** methods.  
You can specify whether to run them on the **true gene trees** or on the **constructed gene trees**.

---

### `Recall_Precision_Evaluation/`

To evaluate recall and precision:

#### Step 1: Generate CSVs for individual simulations
Run the script:
```bash
bash DUPs-recall-prec_run.sh
```
This generates CSV files with recall and precision values for each simulation. You can modify the script to adjust the threshold used for evaluation.

#### Step 2: Compute average recall/precision
Run:
```bash
python dups-TP-avg.py
```
This aggregates the results across simulations and computes averages.

#### Step 3: Generate precision-recall plots
Use:
```bash
python generate_recall_precision_plots_comb.py
```
This produces plots comparing **FastMultRec**, **LCA**, and **MetaEC** across simulations.
