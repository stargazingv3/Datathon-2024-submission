import pandas as pd

# Set file paths
input_file_path = 'Data/AgChange/AgCensus_MasterDataFrame-cleaned.txt'
output_file_path = 'Data/AgChange/AgCensus_MasterDataFrame-overlap.txt'

# Step 1: Read the original data
data = pd.read_table(input_file_path)

# Step 2: Identify the columns to remove
columns_to_remove = [
    'Hrs', 'Shp', 'Flx', 'Hay', 'Ctn', 'Sgc', 'Tbc'
]

# Step 3: Filter out the specified columns
# Keep only the first 9 columns and those that do not match the unwanted abbreviations
filtered_data = data.loc[:, data.columns[:9].tolist() + [col for col in data.columns[9:] if col[:3] not in columns_to_remove]]

# Step 4: Save the filtered data to a new tab-delimited file
filtered_data.to_csv(output_file_path, sep='\t', index=False)

# Print confirmation message
print(f"Filtered data saved to {output_file_path}.")
