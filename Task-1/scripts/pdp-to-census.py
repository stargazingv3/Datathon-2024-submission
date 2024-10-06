import pandas as pd
import json
# Set file paths
analytical_results_file = 'Data/AnalyticalResults-overlap.csv'
commodity_history_file = 'Data/CommodityHistory.csv'
categories_file = 'Data/categories.json'
output_file = 'Data/AnalyticalResults-Census.csv'
# Step 1: Read the analytical results
analytical_results = pd.read_csv(analytical_results_file)
# Step 2: Read the commodity history
commodity_history = pd.read_csv(commodity_history_file)
# Step 3: Read the categories JSON file
with open(categories_file, 'r') as f:
    categories_mapping = json.load(f)
# Step 4: Map commodity codes to AgCensus codes
def map_commodity_code(code):
    # Get the commodity name from the commodity history
    commodity_name = commodity_history.loc[commodity_history['Commodity Code'] == code, 'Commodity Name']
    
    if not commodity_name.empty:
        commodity_name = commodity_name.values[0]  # Get the first match
        
        # Find the corresponding AgCensus code from the JSON mapping
        agcensus_code = categories_mapping.get(commodity_name)
        
        return agcensus_code if agcensus_code else code  # Return the AgCensus code or the original code if not found
    else:
        return code  # Return the original code if no match found
# Step 5: Apply the mapping function to the Commodity Code column
analytical_results['Commodity Code'] = analytical_results['Commodity Code'].apply(map_commodity_code)
# Step 6: Save the updated results to a new CSV file
analytical_results.to_csv(output_file, index=False)
# Print confirmation message
print(f"Updated commodity codes saved to {output_file}.")
