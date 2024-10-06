import pandas as pd
import os

# Directory containing the individual CSV files
input_dir = 'Data'
# Output file path for the combined CSV
output_file = os.path.join(input_dir, 'monarch-adult.csv')

# List to store DataFrames
dataframes = []

# Iterate through each CSV file in the directory
for filename in os.listdir(input_dir):
    if filename.startswith('monarch-adult-') and filename.endswith('.csv'):
        file_path = os.path.join(input_dir, filename)
        # Read the CSV file
        df = pd.read_csv(file_path)
        # Append DataFrame to the list
        dataframes.append(df)

# Concatenate all DataFrames into a single DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv(output_file, index=False)

print(f"All data has been combined into '{output_file}'.")
