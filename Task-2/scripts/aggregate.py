import pandas as pd

# Load the dataset with county information
county_df = pd.read_csv('Data/monarch-adult-county.csv')

# Aggregate sightings by unique fields: Month, Year, Town, State, County, Latitude, Longitude
aggregated_df = county_df.groupby(['Month', 'Year', 'Town', 'State', 'County', 'Latitude', 'Longitude']).agg(
    Total_Sightings=('Number', 'sum')  # Sum the Number field
).reset_index()

# Rename Total_Sightings for clarity
aggregated_df.rename(columns={'Total_Sightings': 'Number'}, inplace=True)

# Save the aggregated DataFrame to a new CSV file
aggregated_df.to_csv('Data/monarch-adult-aggregated.csv', index=False)

print("Aggregated sightings by unique fields have been saved to 'Data/monarch-adult-aggregated.csv'.")
