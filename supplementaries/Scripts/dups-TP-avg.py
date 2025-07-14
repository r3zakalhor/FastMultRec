import os
import pandas as pd

# Function to process a directory and calculate averages
def calculate_averages(directory, metric, t_value):
    accuracy_file = None
    for file in os.listdir(directory):
        #if file.endswith(f'-{metric}-2W-WGD-improvedtrees-bootstrap-b1000-2NumApp-t{t_value}-t200.csv'):
        if file.endswith(f'-{metric}-1W-WGD-unclean-2NumApp-t{t_value}-t200.csv'):
            accuracy_file = os.path.join(directory, file)
            break

    if not accuracy_file:
        print(f"No {metric} CSV file found in {directory} for t{t_value}")
        return None

    df = pd.read_csv(accuracy_file)
    df = df.apply(pd.to_numeric, errors='coerce')  # Convert non-numeric to NaN
    averages = df.mean(numeric_only=True)
    averages['directory'] = os.path.basename(directory)
    return averages

# Function to process all matching directories
def process_directories(base_directory, start_string, metric, t_value, output_file):
    results = []

    for subdir in os.listdir(base_directory):
        full_path = os.path.join(base_directory, subdir)
        if os.path.isdir(full_path) and subdir.startswith(start_string):
            print(f"Processing {metric} for t{t_value} in: {subdir}")
            averages = calculate_averages(full_path, metric, t_value)
            if averages is not None:
                results.append(averages)

    if results:
        df_results = pd.DataFrame(results)
        df_results.to_csv(output_file, index=False)
        print(f"Saved to {output_file}")
    else:
        print(f"No valid data for {metric} t{t_value}, skipping output.")

# Main logic with loops for both metrics and thresholds
if __name__ == "__main__":
    base_directory = os.getcwd()
    start_string = 'sim_1WGD'

    thresholds = [50, 80]
    metrics = ['recall', 'precision']

    for metric in metrics:
        for t_value in thresholds:
            #output_file = f'{metric}-2W-WGD-improvedtrees-bootstrap-b1000-2NumApp-Metaec-t{t_value}-t200-Avg.csv'
            output_file = f'{metric}-1W-WGD-unclean-2NumApp-Metaec-t{t_value}-t200-Avg.csv'
            process_directories(base_directory, start_string, metric, t_value, output_file)
