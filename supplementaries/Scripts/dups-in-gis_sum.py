import os
import pandas as pd
import argparse

def aggregate_csv_files(main_directory, csv_filename):
    # Initialize a dictionary to aggregate data
    aggregated_data = {}

    # Iterate through each subdirectory
    for i in range(1, 101):
        subdirectory = os.path.join(main_directory, f"sim_{i}")
        csv_file_path = os.path.join(subdirectory, csv_filename)
        
        # Read the CSV file if it exists
        if os.path.exists(csv_file_path):
            df = pd.read_csv(csv_file_path)
            
            for _, row in df.iterrows():
                species_id = row['Species ID']
                num_gis = row['Num Gis']
                
                if species_id not in aggregated_data:
                    aggregated_data[species_id] = [0] * 100
                
                aggregated_data[species_id][i-1] = num_gis

    # Convert the aggregated data into a DataFrame
    output_data = []
    for species_id, num_gis_list in aggregated_data.items():
        total_num_gis = sum(num_gis_list)
        output_data.append([species_id, total_num_gis])

    output_df = pd.DataFrame(output_data, columns=['Species ID', 'Num Gis'])

    # Write the output DataFrame to a CSV file in the main directory
    output_csv_path = os.path.join(main_directory, csv_filename)
    output_df.to_csv(output_csv_path, index=False)

    print(f"Aggregated data has been saved to {output_csv_path}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Aggregate CSV data from multiple subdirectories.")
    parser.add_argument("main_directory", help="Path to the main directory containing subdirectories.")
    parser.add_argument("csv_filename", help="Name of the CSV file in each subdirectory.")
    args = parser.parse_args()

    # Call the function with the provided arguments
    aggregate_csv_files(args.main_directory, args.csv_filename)
