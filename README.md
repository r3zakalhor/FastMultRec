

# FastMultRec: Fast Multiple Reconciliation

### Compiling

To compile the FastMultRec program, you can use the classic `cmake` and `make` approach. Here's how:

```bash
mkdir build
cd build
cmake ..
make
```

This will produce the `segrec` executable.

Alternatively, if you'd prefer to compile manually, you can use the following command:

```bash
g++ -std=c++11 -O3 main.cpp define.h genespeciestreeutil.h hashtable.h newicklex.h node.h SegmentalReconciler.h treeinfo.h treeiterator.h util.h genespeciestreeutil.cpp newicklex.cpp node.cpp SegmentalReconciler.cpp treeinfo.cpp treeiterator.cpp -o segrec
```

(Note: You can add additional optimization flags if needed.)

---

### Usage

Here’s an example of how to run the program:

```bash
./segrec -d 5 -l 1 -gf ../data/gene_trees.txt -sf ../data/s_tree.newick -spsep "_" -spindex 0 -o output.txt -al greedy
```

- `-al` specifies the reconciliation algorithm to use. Options are:
  - `simphy`: Use the original mapping from SimPhy.
  - `LCA`: Use the LCA mapping.
  - Any other value will use the **greedy** remapping algorithm.

#### Required Arguments:
- At least one of `-g` or `-gf` must be specified, and at least one of `-s` or `-sf` must be specified.
  - `-g [g1;g2;...;gk]`: Gene trees in Newick format, separated by `;`.
  - `-gf [file]`: File containing gene trees in Newick format (separated by `;`).
  - `-s [newick]`: The species tree in Newick format.
  - `-sf [file]`: File containing the species tree in Newick format.
  - `-al [LCA, simphy, greedy]`: Algorithm to use for reconciliation.

#### Optional Arguments:
- `--help`: Display help message.
- `-d [double]`: Cost for one height of duplication. Default: 3.
- `-l [double]`: Cost for one loss. Default: 1.
- `-h [int]`: Maximum allowed duplication sum-of-heights. Default: 20.
- `-o [file]`: Output file. Default: output to the console.
- `-spsep [string]`: Separator between gene and species in the gene names. Default: `__`.
- `-spindex [int]`: Position of the species in gene names after splitting by the separator. Default: 0.
- `--test`: Run a series of unit tests, including fixed examples and random trees for more complex testing.

---

### SimPhy Integration

#### Postorder Labeling

After simulating with SimPhy, perform a postorder labeling of the species tree:

```bash
python post-order-labeling.py $SpeciesTree $Output_SpeciesTree
```

#### Mapping Gene Trees

Next, map the gene tree nodes based on the SimPhy mapping:

```bash
python map_gene_trees.py $GeneTrees $Output_GeneTrees $Simphy_simulation_directory
```

---

### Running the Segmental Reconciler

The segmental reconciler supports four different algorithms for reconciliation, which can be run to produce the appropriate outputs.

---

### Calculate Distance Between Mappings

To calculate the distance between two mappings, use the following command:

```bash
python compare_mapping.py $firstmapping $secondmapping $SpeciesTree $Output
```

---

### All-in-One Script

For convenience, you can find a bash script that performs all the steps mentioned above in one go. It’s located in `supplementaries/simphy_simulation.sh`.

--- 

This streamlined structure ensures easy compilation and usage while providing clear instructions for running reconciliations with various algorithms.
