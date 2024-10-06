import pandas as pd
import numpy as np

# Set file paths
input_file_path = 'Data/county-selection.csv'
output_file_path = 'Data/county-final.csv'

# Step 1: Load the data
county_data = pd.read_csv(input_file_path)

# Step 2: Initialize a set to track seen counties
seen_counties = {}

# Step 3: List to store modified data
modified_data = []

# Step 4: Define the perturbation distance in miles
perturbation_distance_miles = 10
perturbation_lat = perturbation_distance_miles / 69  # Latitude perturbation in degrees

# Step 5: Process each row in the original DataFrame
for index, row in county_data.iterrows():
    state_code = row['Collection State Code']
    commodity_code = row['Commodity Code']
    county = row['County']
    fips = row['FIPS']
    pesticide_usage = row['Pesticide Usage (ppm)']
    longitude = row['Longitude']
    latitude = row['Latitude']
    
    # Calculate longitude perturbation based on latitude
    latitude_rad = np.radians(latitude)
    perturbation_lon = perturbation_distance_miles / (69 * np.cos(latitude_rad))  # Longitude perturbation in degrees
    
    # Create a unique key for the state and county
    county_key = (state_code, county)
    
    # Check if this county has been seen before
    if county_key in seen_counties:
        # If seen, modify latitude and longitude slightly
        modified_latitude = latitude #+ np.random.uniform(-perturbation_lat, perturbation_lat)
        modified_longitude = longitude #+ np.random.uniform(-perturbation_lon, perturbation_lon)
        
        # Store the modified data
        modified_data.append({
            'Collection State Code': state_code,
            'Commodity Code': commodity_code,
            'County': county,
            'FIPS': fips,
            'Latitude': modified_latitude,
            'Longitude': modified_longitude,
            'Pesticide Usage (ppm)': pesticide_usage
        })
    else:
        # If not seen, add to the set and keep original values
        seen_counties[county_key] = True
        modified_data.append({
            'Collection State Code': state_code,
            'Commodity Code': commodity_code,
            'County': county,
            'FIPS': fips,
            'Latitude': latitude,
            'Longitude': longitude,
            'Pesticide Usage (ppm)': pesticide_usage
        })

# Step 6: Convert the modified data to a DataFrame
modified_df = pd.DataFrame(modified_data)

# Step 7: Group by 'Collection State Code', 'Commodity Code', 'County', and 'FIPS'
# Sum 'Pesticide Usage (ppm)' and take the first longitude and latitude values
consolidated_data = modified_df.groupby(
    ['Collection State Code', 'Commodity Code', 'County', 'FIPS']
).agg(
    {'Pesticide Usage (ppm)': 'sum', 'Longitude': 'first', 'Latitude': 'first'}
).reset_index()

# Step 8: Reorder the columns to have FIPS right after County
consolidated_data = consolidated_data[['Collection State Code', 'Commodity Code', 'County', 'FIPS', 'Latitude', 'Longitude', 'Pesticide Usage (ppm)']]

# Step 9: Save the consolidated data to a new CSV file
consolidated_data.to_csv(output_file_path, index=False)

print(f"Consolidated county pesticide usage saved to {output_file_path}.")
