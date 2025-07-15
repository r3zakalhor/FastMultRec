import matplotlib.pyplot as plt
import pandas as pd
import argparse

def plot_rf_distances(csv_file, output_pdf):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Create the plot
    plt.figure(figsize=(8, 6))
    plt.plot(df["Tree Number"], df["RF Distance"], marker='o', linestyle='-', color='b', alpha=0.7)
    plt.xlabel("Tree Number")
    plt.ylabel("RF Distance")
    plt.title("Robinson-Foulds Distance per Tree Pair")
    plt.grid(True)
    
    # Save the plot
    plt.savefig(output_pdf)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot RF distances from CSV file.")
    parser.add_argument("csv_file", help="Path to the CSV file containing RF distances.")
    parser.add_argument("output_pdf", help="Path to save the output plot as a PDF.")
    
    args = parser.parse_args()
    plot_rf_distances(args.csv_file, args.output_pdf)
