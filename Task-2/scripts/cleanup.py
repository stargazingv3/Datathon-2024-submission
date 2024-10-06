import pandas as pd

# Load the combined DataFrame
df = pd.read_csv('Data/monarch-adult.csv')

# Display the shape before cleanup
print(f"Original Data Shape: {df.shape}")

# Remove rows with missing values
cleaned_df = df.dropna()

# Display the shape after removing missing values
print(f"Shape after removing missing values: {cleaned_df.shape}")

# Define bounds based on the IQR method for outlier detection
Q1 = cleaned_df['Number'].quantile(0.25)
Q3 = cleaned_df['Number'].quantile(0.75)
IQR = Q3 - Q1

print(Q1, Q3)

lower_bound = 0
upper_bound = Q3 + 10 * IQR

# Remove outliers
final_cleaned_df = cleaned_df[(cleaned_df['Number'] >= lower_bound) & (cleaned_df['Number'] <= upper_bound)]

# Display the shape after removing outliers
print(f"Final Cleaned Data Shape: {final_cleaned_df.shape}")

# Save the cleaned DataFrame to a new CSV file
final_cleaned_df.to_csv('Data/monarch-adult-cleaned.csv', index=False)

print("Rows with missing values and outliers have been removed and saved to 'monarch-adult-cleaned.csv'.")
