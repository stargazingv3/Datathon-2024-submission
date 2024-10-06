# The provided dataset only goes to 2020, so re-download the dataset requesting info up to 2022 from PdP:
# Place in Data/AnalyticalResults.csv

# Step 1: Cleanup CSV
echo "Running cleanup-csv.py..."
# Returns a file Data/AnalyticalResults-cleanup1.csv which contains rows that are exactly 16 columns, as specified by the UserGuide
python3 scripts/cleanup-csv.py

# Step 2: Split locations
echo "Running location-split.py..."
# Returns a file Data/AnalyticalResults-cleanup2.csv which contains the first column split into the 7 or 8 fields as specified by the UserGuide
python3 scripts/location-split.py

# Step 3: Crop PDP
echo "Running crop-pdp.py..."
# Returns a file Data/AnalyticalResults-cropped.csv which contains data only for specified years if desired
python3 scripts/crop-pdp.py

# Step 4: Include commodities
echo "Running pdp-include.py..."
# Not all of the crops in the pdp dataset are used in the census dataset, so to cut those out,
# specify a list of commodity names which overlap with the census dataset.
# The Commodity Code lookup table is located at Data/CommodityHistory.csv.
# Returns a file Data/AnalyticalResults-overlap.csv which now contains crops which overlap with the census data
python3 scripts/pdp-include.py

# Step 5: Filter TXT
echo "Running filter-txt.py..."
# Returns a file Data/AgChange/AgCensus_MasterDataFrame-cropped.txt which contains data from years of interest.
# The census dataset contains information from as far back as 1840, so this will by default only consider data since 1992.
python3 scripts/filter-txt.py

# Step 6: Cleanup TXT
echo "Running cleanup-txt.py..."
# Returns a file Data/AgChange/AgCensus_MasterDataFrame-cleaned.txt which ensures that each line has the same number of columns,
# which is 84 for the number of years we selected.
# Please disregard the bug saying the number of files removed is the same as the total number of files.
python3 scripts/cleanup-txt.py

# Step 7: Exclude census
echo "Running census-exclude.py..."
# Returns a file Data/AgChange/AgCensus_MasterDataFrame-overlap.txt which removes crops that are in the census but not in the pdp dataset
python3 scripts/census-exclude.py

# Step 8: PDP to Census
echo "Running pdp-to-census.py..."
# Returns a file Data/AnalyticalResults-Census.csv where the pdp dataset's commodity codes are updated to be that of the census dataset
python3 scripts/pdp-to-census.py

# Manipulation/Analysis

# Step 9: Select by year for PDP
echo "Running select-by-year-PdP.py..."
# Returns a file Data/AnalyticalResults-Census-2017.csv which contains data for only the year 2017
python3 scripts/select-by-year-PdP.py

# Step 10: County rankings normalized
echo "Running county-rankings-normalized.py..."
# Returns a file Data/AgChange/County_Crop_Hotspots_2017.json which contains a JSON dict ranking each county for each crop and state
# according to their odds of producing said crop. This is based on the standard deviation of the county's crop production
# compared to the average in that state, stored in probability format.
# By default, only runs for data in 2017.
python3 scripts/county-rankings-normalized.py

# Step 11: County selection
echo "Running county-selection.py..."
# Returns a file Data/county-selection.csv where the modified pdp dataset is now appended a county and FIPS code of that county.
# This is determined using the dict returned by the prior command.
# For each row of the pdp dataset, the state and commodity code (now census' commodity code) are searched in the dictionary.
# A county is selected according to its weighted probability of being selected for that crop.
python3 scripts/county-selection.py

# Step 12: Consolidate
echo "Running consolidate.py..."
# Returns a file Data/county-final.csv which consolidates the pesticide usage by county.
python3 scripts/consolidate.py

# Step 13: Task 1
echo "Running task1.py..."
# Returns a file task1.png which is a coloring of U.S. counties by pesticide usage.
# It is slightly flawed in that very low concentration areas are not visible.
python3 scripts/task1.py

# Assumptions/Decisions Made
# Disregard what type of pesticide

echo "All scripts have been executed successfully!"