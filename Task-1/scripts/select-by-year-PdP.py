import pandas as pd

# Set file paths
input_file_path = 'Data/AnalyticalResults-Census.csv'
output_file_path = 'Data/AnalyticalResults-Census-2017.csv'

# Step 1: Read the analytical results data
data = pd.read_csv(input_file_path)

# Step 2: Filter the data for the year 2022
filtered_data = data[data['Year'] == 17]

# Step 3: Save the filtered data to a new CSV file
filtered_data.to_csv(output_file_path, index=False)

print(f"Filtered data for the year 2022 saved to {output_file_path}.")
