import pandas as pd

# Load the CSV file
file_path = 'Data/AnalyticalResults-cleanup1.csv'
df = pd.read_csv(file_path)

# Function to split the Sample ID
def split_sample_id(sample_id):
    length = len(sample_id)
    
    if length == 17:
        collection_state_code = sample_id[0:2]        # 2-letter Collection State code
        year = sample_id[2:4]                          # 2-digit Year
        month = sample_id[4:6]                         # 2-digit Month
        day = sample_id[6:8]                           # 2-digit Day
        collection_site_code = sample_id[8:12]        # 4-digit Collection Site code
        commodity_code = sample_id[12:14]              # 2-letter Commodity code
        analyzing_lab_code = sample_id[14:17]         # 3-character Analyzing Lab code
        source_id = None                                # No Source ID for 17 characters
        
        return [collection_state_code, year, month, day, collection_site_code, commodity_code, analyzing_lab_code, source_id]
    
    elif length == 18:
        collection_state_code = sample_id[0:2]        # 2-letter Collection State code
        year = sample_id[2:4]                          # 2-digit Year
        month = sample_id[4:6]                         # 2-digit Month
        day = sample_id[6:8]                           # 2-digit Day
        collection_site_code = sample_id[8:12]        # 4-digit Collection Site code
        commodity_code = sample_id[12:14]              # 2-letter Commodity code
        analyzing_lab_code = sample_id[14:17]         # 3-character Analyzing Lab code
        source_id = sample_id[17]                      # 1-letter Source ID code
        
        return [collection_state_code, year, month, day, collection_site_code, commodity_code, analyzing_lab_code, source_id]

    return [None] * 8  # Ensure 8 columns returned if format is not as expected

# Create new DataFrame for the results
new_columns = ['Collection State Code', 'Year', 'Month', 'Day', 'Collection Site Code', 'Commodity Code', 'Analyzing Lab Code', 'Source ID']
new_data = df['Sample ID'].apply(split_sample_id).tolist()

# Create a new DataFrame with the split data
new_df = pd.DataFrame(new_data, columns=new_columns)

# Append the original columns to the new DataFrame (excluding the Sample ID)
result_df = pd.concat([new_df, df.drop(columns=['Sample ID'])], axis=1)

# Save the new DataFrame to a CSV file
output_file_path = 'Data/AnalyticalResults-cleanup2.csv'
result_df.to_csv(output_file_path, index=False)

print(f"Data has been successfully split and saved to {output_file_path}.")
