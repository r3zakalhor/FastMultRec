# FastMultRec: Fast Multiple gene trees Reconciliation program

### Compiling

To compile the FastMultRec program, you can use the `cmake` and `make` approach as follows:

```bash
mkdir build
cd build
cmake ..
make
```

This will produce the `FastMultRec` executable.

Alternatively, to compile manually, use this command:

```bash
g++ -std=c++11 -O3 main.cpp define.h genespeciestreeutil.h hashtable.h newicklex.h node.h SegmentalReconciler.h treeinfo.h treeiterator.h util.h ReconciliationTester.h genespeciestreeutil.cpp newicklex.cpp node.cpp SegmentalReconciler.cpp treeinfo.cpp treeiterator.cpp ReconciliationTester.cpp -o FastMultRec
```

(Note: Additional optimization flags can be added if required.)

---

### Usage

To run the program, use the following example command:

```bash
./FastMultRec -d 5 -l 1 -gf ../data/gene_trees.txt -sf ../data/s_tree.newick -spsep "_" -spindex 0 -o output.txt -al FastMultRec
```

- `-al` specifies the reconciliation algorithm. Options:
  - `simphy`: Use the original mapping from SimPhy.
  - `LCA`: Use the LCA mapping.
  - Any other value: Use the **FastMultRec** remapping algorithm.

#### Required Arguments:
- At least one of `-g` or `-gf` must be provided, and at least one of `-s` or `-sf` must be provided.
  - `-g [g1;g2;...;gk]`: Gene trees in Newick format, separated by `;`.
  - `-gf [file]`: File containing gene trees in Newick format, separated by `;`.
  - `-s [newick]`: Species tree in Newick format.
  - `-sf [file]`: File containing the species tree in Newick format.
  - `-al [LCA, simphy, FastMultRec]`: Algorithm to use for reconciliation.

#### Optional Arguments:
- `--help`: Display help message.
- `-d [double]`: Cost for one height of duplication. Default: 3.
- `-l [double]`: Cost for one loss. Default: 1.
- `-h [int]`: Maximum allowed duplication sum-of-heights. Default: 20.
- `-o [file]`: Output file. Default: output to console.
- `-spsep [string]`: Separator between gene and species in gene names. Default: `__`.
- `-spindex [int]`: Position of the species in gene names after splitting by the separator. Default: 0.
- `--test`: Run a series of unit tests, including fixed examples and random trees for more complex testing.

---

### SimPhy

https://github.com/adamallo/SimPhy/wiki/Manual

#### Simulating with WGD and Applying Fractionation

Use the script `supplementaries/simulate_1WGD_simphy.sh` to insert a WGD event into a SimPhy simulation and apply fractionation. This script makes use of the following Python scripts:
- `map_gene_trees_oneWGD.py`
- `apply_losses_on_simphy.py`
- `post-order-labeling.py`

**Note**: `map_gene_trees_oneWGD.py` may need to be modified to handle different numbers of WGDs based on filenames in SimPhy simulation directories.

#### Analyzing a SimPhy Simulation Directory

Use the script `supplementaries/analyze_sims_parallel.sh` to calculate the path distances between different mappings (e.g., between LCA and SimPhy or between LCA and FastMultRec with varying duplication costs). This script relies on `compare_mapping.py`.

#### Calculating Recall and Precision

To calculate recall and precision for duplications, follow these steps:
1. Run `supplementaries/dups-in-gis_run.sh` to calculate the number of gene trees supporting duplications at each species (uses `dups-in-gis.py`).
2. Call `supplementaries/DUPs-recall-prec_run.sh` to calculate recall and precision (uses `DUPs-recall-prec-V2.py`).

#### Applying NNIs to SimPhy Simulations

Use the script `supplementaries/apply_NNIs.sh` to apply NNIs (Nearest Neighbor Interchanges) to SimPhy simulations. You can set the number of NNIs applied to each gene tree via the `k` parameter in the script. This script uses `apply_NNIs.py`.



### Stochastic Version

To run the stochastic version of FastMultRec, use the following command:

```bash
./FastMultRec -d 5 -l 1 -gf ../data/gene_trees.txt -sf ../data/s_tree.newick -spsep "_" -spindex 0 -o output.txt -al stochastic -tmp 1 -stoloops 2000
```

#### Parameters:
- `-d [double]`: Cost for one height of duplication.
- `-l [double]`: Cost for one loss.
- `-gf [file]`: File containing gene trees in Newick format, separated by `;`.
- `-sf [file]`: File containing the species tree in Newick format.
- `-spsep [string]`: Separator between gene and species in gene names (default: `__`).
- `-spindex [int]`: Position of the species in gene names after splitting by the separator (default: 0).
- `-o [file]`: Output file.
- `-al [stochastic]`: Specifies the use of the stochastic reconciliation algorithm.
- `-tmp [double]`: Specifies the temperature value for the stochastic algorithm.
- `-stoloops [int]`: Number of loops after which the algorithm stops if no improvement is detected.


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


