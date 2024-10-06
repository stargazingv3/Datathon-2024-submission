import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# File paths
pesticide_data_path = 'Data/county-final.csv'
county_shapefile_path = 'Data/AgChange/shapefiles/US_counties_2012_geoid.shp'  # You'll need to provide this
output_image_path = 'task1.png'

# Step 1: Load the pesticide usage data
pesticide_data = pd.read_csv(pesticide_data_path)

# Step 2: Load the U.S. counties shapefile
counties = gpd.read_file(county_shapefile_path)

# Step 3: Ensure FIPS columns are of the same type
# Convert FIPS to string in both DataFrames
counties['FIPS'] = counties['FIPS'].astype(str)
pesticide_data['FIPS'] = pesticide_data['FIPS'].astype(str)

# Merge pesticide data with county geometries
merged_data = counties.merge(pesticide_data, left_on='FIPS', right_on='FIPS', how='left')

# Step 4: Create the map
# Step 4: Create the map
fig, ax = plt.subplots(figsize=(20, 12))

# Define the minimum and maximum for the color scale
vmin = merged_data['Pesticide Usage (ppm)'].min()  # Minimum pesticide usage
vmax = merged_data['Pesticide Usage (ppm)'].max()  # Maximum pesticide usage

# Plot counties, coloring by pesticide usage
merged_data.plot(column='Pesticide Usage (ppm)', 
                 ax=ax, 
                 legend=True,
                 legend_kwds={'label': 'Pesticide Usage (ppm)', 'orientation': "horizontal"},
                 cmap='OrRd',
                 missing_kwds={'color': 'lightgrey'},
                 vmin=vmin,
                 vmax=vmax)

# Optionally adjust the colormap
# If you want to enhance visibility of low values, consider using 'YlOrRd' or 'YlGn'

# Remove axis
ax.axis('off')

# Add title
plt.title('Pesticide Usage by County: 2017', fontsize=16)

# Step 5: Save the figure
plt.savefig(output_image_path, bbox_inches='tight', dpi=300)
plt.close()

print(f"Map saved to {output_image_path}.")

