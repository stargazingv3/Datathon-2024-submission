import pandas as pd
import csv  # Import the standard CSV module

# Load the dataset, specifying low_memory=False to avoid DtypeWarning
data_path = 'Data/AnalyticalResults-cleanup2.csv'
df = pd.read_csv(data_path, low_memory=False)

# Specify the last two digits of the years you are interested in
years_of_interest = ['97', '98', '99', '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22']

# Convert the 'Year' column to string to match the last two digits
df['Year'] = df['Year'].astype(str).str[-2:]

# Filter the DataFrame based on the specified years
filtered_df = df[df['Year'].isin(years_of_interest)].copy()  # Use .copy() to avoid SettingWithCopyWarning

# Quote the 'Year' column for the years of interest
filtered_df['Year'] = filtered_df['Year'].apply(lambda x: f'{x}' if x in years_of_interest else x)

# Save the filtered DataFrame to a new CSV file without quoting any other fields
filtered_data_path = 'Data/AnalyticalResults-cropped.csv'
filtered_df.to_csv(filtered_data_path, index=False, quoting=csv.QUOTE_NONE)

print(f"Filtered dataset has been saved to '{filtered_data_path}'.")
