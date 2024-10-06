import pandas as pd

# Load the combined DataFrame
df = pd.read_csv('Data/monarch-adult-cleaned.csv')

# Function to check for missing values
def check_missing_values(dataframe):
    missing_count = dataframe.isnull().sum()
    missing_percentage = (missing_count / len(dataframe)) * 100
    missing_info = pd.DataFrame({'Missing Count': missing_count, 'Missing Percentage': missing_percentage})
    return missing_info[missing_info['Missing Count'] > 0]

# Function to check for outliers in the "Number" field and return statistics
def check_outliers(dataframe, column_name):
    Q1 = dataframe[column_name].quantile(0.25)
    Q3 = dataframe[column_name].quantile(0.75)
    IQR = Q3 - Q1
    
    # Define bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Statistics
    stats = {
        'Mean': dataframe[column_name].mean(),
        'Standard Deviation': dataframe[column_name].std(),
        'Minimum': dataframe[column_name].min(),
        'Maximum': dataframe[column_name].max(),
        'Q1': Q1,
        'Q3': Q3,
        'IQR': IQR,
        'Lower Bound': lower_bound,
        'Upper Bound': upper_bound
    }
    
    # Count outliers
    outlier_count = dataframe[(dataframe[column_name] < lower_bound) | (dataframe[column_name] > upper_bound)].shape[0]
    
    stats['Outlier Count'] = outlier_count
    
    return stats

# Check missing values
missing_values = check_missing_values(df)
print("Missing Values:")
print(missing_values)

# Check for outliers in the "Number" field
number_column = 'Number'  # Change this to the exact name of your column if it's different
outlier_stats = check_outliers(df, number_column)

print(f"\nOutlier Statistics for '{number_column}':")
for stat_name, value in outlier_stats.items():
    print(f"{stat_name}: {value}")
