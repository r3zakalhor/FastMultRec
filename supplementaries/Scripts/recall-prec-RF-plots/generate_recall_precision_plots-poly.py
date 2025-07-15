import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

def plot_polynomials(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Extract data
    x_values = df.iloc[:, -1].values  # Last column as x-values (names)
    names = df.columns[1:-1]  # Names for the curves from the columns (excluding the first and last columns)
    
    # Create the plots
    plt.figure(figsize=(12, 8))
    
    for name in names:
        y_values = df[name].values  # Get y-values for the polynomial
        # Convert x_values to numerical values for fitting
        x_numeric = np.arange(len(x_values))
        # Fit a polynomial of order 6
        coefficients = np.polyfit(x_numeric, y_values, 1)
        polynomial = np.poly1d(coefficients)
        # Generate x values for plotting the polynomial curve
        x_range = np.linspace(0, len(x_values) - 1, 500)
        plt.plot(x_range, polynomial(x_range), label=name)
    
    # Add labels and legend
    plt.xticks(ticks=np.arange(len(x_values)), labels=x_values, rotation=90)
    plt.xlabel('Directories')
    plt.ylabel('Polynomial Fit')
    plt.title('Polynomial Fits of the Data')
    plt.legend()
    
    # Ensure 'plots' directory exists
    if not os.path.exists('plots'):
        os.makedirs('plots')
    
    # Save plot as PDF with the same name as the CSV file
    base_name = os.path.splitext(os.path.basename(csv_file))[0]
    pdf_file = os.path.join('plots', f'{base_name}.pdf')
    plt.savefig(pdf_file, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    plot_polynomials(csv_file)
