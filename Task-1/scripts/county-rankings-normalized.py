import pandas as pd
import json

# Set file paths
input_file_path = 'Data/AgChange/AgCensus_MasterDataFrame-overlap.txt'

# Step 1: Read the filtered data
data = pd.read_table(input_file_path)

# Step 2: Select relevant crop columns for 2017
crop_columns = [col for col in data.columns if col[:3] in ['Brl', 'Crn', 'Oat', 'Pnt', 'Swt', 'Pls', 'Soy', 'Tky', 'Cat', 'Swn', 'Ric', 'Wht'] and col.endswith('2017')]

# Step 3: Melt the DataFrame to long format for easier calculations
melted_data = data.melt(id_vars=['STATE', 'COUNTY'], value_vars=crop_columns, var_name='CropYear', value_name='Production')

# Extract the crop abbreviation and year from the CropYear column
melted_data['Crop'] = melted_data['CropYear'].str[:3]
melted_data['Year'] = melted_data['CropYear'].str[3:]

# Step 4: Calculate average production by county and state
county_avg = melted_data.groupby(['STATE', 'COUNTY', 'Crop'])['Production'].mean().reset_index()
state_avg = melted_data.groupby(['STATE', 'Crop'])['Production'].mean().reset_index().rename(columns={'Production': 'State_Avg_Production'})

# Step 5: Merge to get both county and state averages
merged_data = pd.merge(county_avg, state_avg, on=['STATE', 'Crop'])

# Step 6: Calculate deviation from state average
merged_data['Deviation'] = merged_data['Production'] - merged_data['State_Avg_Production']

# Step 7: Create a score based on production relative to the state average
merged_data['Score'] = merged_data['Production'] / merged_data['State_Avg_Production']

# Step 8: Normalize the scores within each crop for each state
merged_data['Probability'] = merged_data.groupby(['STATE', 'Crop'])['Score'].transform(lambda x: x / x.sum())

# Step 9: Replace NaN values with 0
merged_data.fillna(0, inplace=True)

# Step 10: Prepare the output structure
output_dict = {}

for state, state_data in merged_data.groupby('STATE'):
    output_dict[state] = {}
    for crop, crop_data in state_data.groupby('Crop'):
        output_dict[state][crop] = crop_data[['COUNTY', 'Deviation', 'Probability']].set_index('COUNTY').to_dict(orient='index')
        for county in output_dict[state][crop]:
            output_dict[state][crop][county] = {
                "Deviation": output_dict[state][crop][county]['Deviation'],
                "Probability": output_dict[state][crop][county]['Probability']
            }

# Step 11: Save the output as a JSON file
output_file_path = 'Data/AgChange/County_Crop_Hotspots_2017.json'
with open(output_file_path, 'w') as json_file:
    json.dump(output_dict, json_file, indent=4)

print(f"Hotspot analysis for 2017 saved to {output_file_path}.")
