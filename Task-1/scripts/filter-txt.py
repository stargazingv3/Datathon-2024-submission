import pandas as pd

# Set the path to the original Ag Census Master Data file
file_path = "Data/AgChange/AgCensus_MasterDataFrame.txt"

# Read the data
ag_data = pd.read_csv(file_path, sep='\t')

# Specify the years of interest
years_of_interest = [1992, 2002, 2012, 2017]

# Extract the year columns (assuming the first 475 columns are crop/animal data)
year_columns = ag_data.columns[:475]  # Adjust based on the actual data structure

# Initialize lists for selected years and logging
selected_years = []
failed_extractions = []
failure_count = 0

# Filter columns based on specified years
for col in year_columns:
    # Check if the column name has a valid year part
    if len(col) >= 7:  # Ensure there's enough length to extract the year
        year_str = col[3:7]  # Extract YYYY
        try:
            year = int(year_str)  # Convert to integer
            if year in years_of_interest:
                selected_years.append(col)
        except ValueError:
            failed_extractions.append(col)  # Log the failed column
            failure_count += 1  # Increment the failure count
    else:
        failed_extractions.append(col)  # Log the column with insufficient length
        failure_count += 1

# Prepare the filtered DataFrame
filtered_ag_data = ag_data[['STATE', 'COUNTY', 'FIPS', 'STCTY', 'AREA_KM', 'Bailey_Eco', 'USDA_FRR', 'Lon', 'Lat'] + selected_years]

# Set the output file path
output_file_path = "Data/AgChange/AgCensus_MasterDataFrame-cropped.txt"

# Write the filtered data to a new tab-delimited file
filtered_ag_data.to_csv(output_file_path, sep='\t', index=False, quoting=3)  # quoting=3 is equivalent to csv.QUOTE_NONE

# Print confirmation message
print("Filtered data saved as AgCensus_MasterDataFrame-cropped.txt")
print(f"Number of failed extractions: {failure_count}")

# Log failed extractions
if failure_count > 0:
    with open("Data/AgChange/extraction_errors.log", "w") as log_file:
        for failed_col in failed_extractions:
            log_file.write(f"Failed to process column: {failed_col}\n")
