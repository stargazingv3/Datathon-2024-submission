import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import r2_score, mean_squared_error

# Set the plotting backend to avoid threading issues
plt.switch_backend('Agg')

# Load the monarch dataset
monarch_data_path = 'Data/monarch-adult-aggregated.csv'
monarch_df = pd.read_csv(monarch_data_path)

# Load the pesticide usage dataset
pesticide_data_path = 'Data/county-final.csv'
pesticide_df = pd.read_csv(pesticide_data_path)

# Create a list of years to analyze (from 2010 to 2022)
years_to_analyze = list(range(2010, 2023))

# Initialize lists to store metrics
metrics = []

# Create the plots directory if it doesn't exist
os.makedirs('plots', exist_ok=True)

for year in years_to_analyze:
    # Filter monarch data for the specific year
    monarch_year = monarch_df[monarch_df['Year'] == year]

    # Aggregate monarch sightings by county for the year
    monarch_count_by_county = monarch_year.groupby('County').agg(
        Total_Sightings=('Number', 'sum')
    ).reset_index()

    # Convert county names to lowercase for case-insensitive matching
    monarch_count_by_county['County'] = monarch_count_by_county['County'].str.lower()
    pesticide_df['County'] = pesticide_df['County'].str.lower()

    # Find common counties
    common_counties = set(monarch_count_by_county['County']).intersection(set(pesticide_df['County']))

    # Filter both DataFrames to include only common counties
    monarch_filtered = monarch_count_by_county[monarch_count_by_county['County'].isin(common_counties)]
    pesticide_filtered = pesticide_df[pesticide_df['County'].isin(common_counties)]

    # Merge with pesticide data
    merged_df = monarch_filtered.merge(
        pesticide_filtered[['County', 'Pesticide Usage (ppm)']],
        on='County',
        how='inner'
    )

    # Check if merged_df has enough data to perform analysis
    if merged_df.shape[0] > 1:
        X = merged_df[['Pesticide Usage (ppm)']]
        y = merged_df['Total_Sightings']

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Check if there are enough samples in the training set for GridSearchCV
        if len(y_train) >= 2:
            # Random Forest Regression with hyperparameter tuning
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [None, 10, 20, 30],
                'min_samples_split': [2, 5],
                'min_samples_leaf': [1, 2],
                'bootstrap': [True, False]
            }

            # Set cv to a minimum of 2
            n_splits = 3  # Use a fixed number of splits
            
            rf_model = RandomForestRegressor(random_state=42)
            grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, 
                                       cv=n_splits, n_jobs=-1, verbose=2, scoring='r2')
            grid_search.fit(X_train, y_train)

            # Best parameters
            best_rf_model = grid_search.best_estimator_
            predictions_rf = best_rf_model.predict(X_test)

            # Metrics
            r2 = r2_score(y_test, predictions_rf)
            rmse = mean_squared_error(y_test, predictions_rf, squared=False)

            # Store metrics
            metrics.append({'year': year, 'r2': r2, 'rmse': rmse})

            print(f"Year: {year}, R²: {r2:.4f}, RMSE: {rmse:.4f}")

            # Feature Importance
            importances = best_rf_model.feature_importances_
            feature_names = X.columns

            # Plotting Feature Importance
            plt.figure(figsize=(8, 5))
            plt.barh(feature_names, importances)
            plt.title(f'Feature Importance for Year {year}')
            plt.xlabel('Importance')
            plt.ylabel('Features')
            plt.savefig(f'plots/Feature_Importance_{year}.png')
            plt.close()  # Close the plot to avoid display
        else:
            # If not enough training samples, train without tuning
            rf_model = RandomForestRegressor(random_state=42, n_estimators=100)
            rf_model.fit(X_train, y_train)
            predictions_rf = rf_model.predict(X_test)

            # Metrics
            r2 = r2_score(y_test, predictions_rf)
            rmse = mean_squared_error(y_test, predictions_rf, squared=False)

            # Store metrics
            metrics.append({'year': year, 'r2': r2, 'rmse': rmse})

            print(f"Year: {year}, Not enough data for tuning. R²: {r2:.4f}, RMSE: {rmse:.4f}")

    else:
        print(f"Year: {year}, Not enough data for analysis.")

# Report average metrics across years
average_r2 = np.mean([metric['r2'] for metric in metrics if 'r2' in metric])
average_rmse = np.mean([metric['rmse'] for metric in metrics if 'rmse' in metric])

print("\nAverage Metrics from 2010 to 2022:")
print(f"Average R²: {average_r2:.4f}, Average RMSE: {average_rmse:.4f}")
