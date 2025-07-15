import sys
import pandas as pd
import matplotlib.pyplot as plt

def plot_box(csv_file, output_pdf):
    df = pd.read_csv(csv_file)
    
    # Assuming the RF distances are in the second column
    values = df.iloc[:,1]

    plt.figure()
    plt.boxplot(values, vert=True, patch_artist=True)
    plt.title("Box plot of RF distances")
    plt.ylabel("RF Distance")

    plt.savefig(output_pdf)
    plt.close()

if __name__ == "__main__":
    plot_box(sys.argv[1], sys.argv[2])
