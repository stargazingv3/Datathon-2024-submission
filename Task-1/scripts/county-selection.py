import pandas as pd
import json
import numpy as np

# Set file paths
analytical_results_file = 'Data/AnalyticalResults-Census-2017.csv'
county_probabilities_file = 'Data/AgChange/County_Crop_Hotspots_2017.json'
ag_census_file = 'Data/AgChange/AgCensus_MasterDataFrame-overlap.txt'
output_file = 'Data/county-selection.csv'

# Step 1: Load the data
analytical_results = pd.read_csv(analytical_results_file)
with open(county_probabilities_file, 'r') as f:
    county_probabilities = json.load(f)

# Load Ag Census data for latitude, longitude, and FIPS
ag_census_data = pd.read_table(ag_census_file)

# Step 2: Prepare a DataFrame to store results
results = []

# Step 3: Iterate through each row of the pesticide data
for index, row in analytical_results.iterrows():
    state_code = row['Collection State Code']
    commodity_code = row['Commodity Code']
    
    # Get the crop abbreviation
    crop = commodity_code
    
    # Check if state and crop exist in the probabilities dictionary
    if state_code in county_probabilities and crop in county_probabilities[state_code]:
        counties = county_probabilities[state_code][crop]
        
        # Create a list of counties and their probabilities
        county_list = list(counties.keys())
        probabilities = [counties[county]['Probability'] for county in county_list]
        
        # Normalize probabilities to sum to 1
        probabilities = np.array(probabilities) / np.sum(probabilities)
        
        # Select a county based on the probabilities
        selected_county = np.random.choice(county_list, p=probabilities)
        
        # Get the latitude, longitude, and FIPS for the selected county
        county_info = ag_census_data[(ag_census_data['STATE'] == state_code) & (ag_census_data['COUNTY'] == selected_county)]
        if not county_info.empty:
            latitude = county_info['Lat'].values[0]
            longitude = county_info['Lon'].values[0]
            fips = county_info['FIPS'].values[0]  # Get the FIPS code
            
            # Convert concentration to ppm
            concentration = row['Concentration']
            lod = row['LOD']
            unit = row['pp_']

            if unit == 'M':  # Parts per million
                normalized_concentration = concentration
            elif unit == 'B':  # Parts per billion
                normalized_concentration = concentration / 1000  # Convert to ppm
            elif unit == 'T':  # Parts per trillion
                normalized_concentration = concentration / 1_000_000  # Convert to ppm
            else:
                normalized_concentration = 0  # Default to 0 if unknown unit
            
            # Append the result to the results list
            results.append({
                'Collection State Code': state_code,
                'Commodity Code': commodity_code,
                'County': selected_county,
                'FIPS': fips,
                'Latitude': latitude,
                'Longitude': longitude,
                'Pesticide Usage (ppm)': normalized_concentration
            })

# Step 4: Convert results to a DataFrame and save to CSV
results_df = pd.DataFrame(results)
results_df.to_csv(output_file, index=False)

print(f"Task 1 results with pesticide usage and FIPS saved to {output_file}.")
