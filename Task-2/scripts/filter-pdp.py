import pandas as pd

# Load the dataset
data_path = 'Data/AnalyticalResults-census-16-split.csv'
df = pd.read_csv(data_path)

# Filter for relevant columns
filtered_df = df[['Collection State Code', 'Year', 'Month', 'Concentration', 'pp_']]

# Normalize Concentration based on pp_ unit
def normalize_concentration(row):
    if row['pp_'] == 'M':  # parts-per-million
        return row['Concentration']
    elif row['pp_'] == 'B':  # parts-per-billion
        return row['Concentration'] / 1000  # Convert pp-billion to ppm
    elif row['pp_'] == 'T':  # parts-per-trillion
        return row['Concentration'] / 1000000  # Convert pp-trillion to ppm
    else:
        return None  # Handle unexpected units

# Apply normalization
filtered_df['Normalized_Concentration'] = filtered_df.apply(normalize_concentration, axis=1)

# Drop rows with missing normalized concentration values
filtered_df.dropna(subset=['Normalized_Concentration'], inplace=True)

# Select final columns to keep
final_df = filtered_df[['Collection State Code', 'Year', 'Month', 'Normalized_Concentration']]

# Save the new dataset to a CSV file
final_df.to_csv('Data/filtered-pdp.csv', index=False)

print("Normalized pesticide dataset has been saved to 'Data/filtered-pdp.csv'.")
