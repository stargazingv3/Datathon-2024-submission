import pandas as pd

# Load the cleaned monarch dataset
cleaned_df = pd.read_csv('Data/monarch-adult-cleaned.csv')

# Load the US cities dataset
us_cities_df = pd.read_csv('Data/uscities.csv')

# Convert town and city names to lowercase for case-insensitive matching
cleaned_df['Town'] = cleaned_df['Town'].str.lower()
us_cities_df['city'] = us_cities_df['city'].str.lower()

# Merge the datasets on the 'Town' and 'State' fields
merged_df = cleaned_df.merge(
    us_cities_df[['city', 'state_id', 'county_name', 'lat', 'lng']],  # Keep relevant columns
    left_on=['Town', 'State'],
    right_on=['city', 'state_id'],
    how='inner'  # Use an inner join to keep only matched records
)

# Select the specified columns for the final output
final_df = merged_df[['Month', 'Year', 'Town', 'State', 'county_name', 'lat', 'lng', 'Number']]

# Rename the columns appropriately
final_df.rename(columns={'county_name': 'County', 'lat': 'Latitude', 'lng': 'Longitude'}, inplace=True)

# Save the final DataFrame to a new CSV file
final_df.to_csv('Data/monarch-adult-county.csv', index=False)

# Calculate the number of ignored rows
ignored_rows_count = cleaned_df.shape[0] - merged_df.shape[0]

print(f"Filtered dataset with county information has been saved to 'Data/monarch-adult-county.csv'.")
print(f"Number of rows ignored due to no match: {ignored_rows_count}.")
