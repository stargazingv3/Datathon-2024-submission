import pandas as pd

# Set file paths
analytical_results_file = 'Data/AnalyticalResults-cropped.csv'
commodity_history_file = 'Data/CommodityHistory.csv'
include_file = 'Data/include.txt'  # Changed from exclude.txt to include.txt
output_file = 'Data/AnalyticalResults-overlap.csv'

# Step 1: Read the analytical results and commodity history
analytical_results = pd.read_csv(analytical_results_file)
commodity_history = pd.read_csv(commodity_history_file)

# Step 2: Read the include list and get the commodity codes
with open(include_file, 'r') as f:
    include_commodities = {line.strip() for line in f if line.strip()}

# Step 3: Map commodity names to codes and filter in included codes
# Create a set of commodity codes to include
included_codes = set(commodity_history.loc[commodity_history['Commodity Name'].isin(include_commodities), 'Commodity Code'])

# Step 4: Count the total number of rows in the original dataset
total_rows = len(analytical_results)

# Step 5: Filter the analytical results to include only the specified commodity codes
filtered_results = analytical_results[analytical_results['Commodity Code'].isin(included_codes)]

# Step 6: Count the number of excluded rows
excluded_rows_count = total_rows - len(filtered_results)

# Step 7: Save the filtered results to a new CSV file
filtered_results.to_csv(output_file, index=False)

# Print the counts
print(f"Total number of rows in the original dataset: {total_rows}")
print(f"Number of rows excluded: {excluded_rows_count}")
print(f"Filtered results saved to {output_file}.")
