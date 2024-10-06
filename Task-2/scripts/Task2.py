import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.ensemble import RandomForestRegressor

# Load the monarch dataset
monarch_data_path = 'Data/monarch-adult-aggregated.csv'
monarch_df = pd.read_csv(monarch_data_path)

# Load the pesticide usage dataset
pesticide_data_path = 'Data/county-final.csv'
pesticide_df = pd.read_csv(pesticide_data_path)

# Create a list of years to analyze (from 1997 to 2022)
years_to_analyze = list(range(1997, 2023))  # Years from 1997 to 2022

# Initialize dictionaries to store metrics and lists for aggregation
metrics = {
    'linear': {'r2': [], 'rmse': []},
    'polynomial': {'r2': [], 'rmse': []},
    'log-linear': {'r2': [], 'rmse': []},
    'log-polynomial': {'r2': [], 'rmse': []},
    'random-forest': {'r2': [], 'rmse': []},
}

# Initialize lists for total sightings and pesticide usage with None values
total_sightings_by_year = [None] * len(years_to_analyze)
total_usage_by_year = [None] * len(years_to_analyze)

# Create the plots directory if it doesn't exist
os.makedirs('plots', exist_ok=True)

# Open a file to write results
with open('results.txt', 'w') as results_file:
    for idx, year in enumerate(years_to_analyze):
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

            # Store totals for the year
            total_sightings_by_year[idx] = y.sum()
            total_usage_by_year[idx] = X['Pesticide Usage (ppm)'].sum()

            # Linear Regression
            linear_model = LinearRegression()
            linear_model.fit(X, y)
            predictions_linear = linear_model.predict(X)
            metrics['linear']['r2'].append(r2_score(y, predictions_linear))
            metrics['linear']['rmse'].append(mean_squared_error(y, predictions_linear, squared=False))

            # Polynomial Regression
            poly = PolynomialFeatures(degree=2)
            X_poly = poly.fit_transform(X)
            polynomial_model = LinearRegression()
            polynomial_model.fit(X_poly, y)
            predictions_poly = polynomial_model.predict(X_poly)
            metrics['polynomial']['r2'].append(r2_score(y, predictions_poly))
            metrics['polynomial']['rmse'].append(mean_squared_error(y, predictions_poly, squared=False))

            # Log-Linear Regression
            merged_df['Log_Total_Sightings'] = np.log(merged_df['Total_Sightings'])
            log_linear_model = LinearRegression()
            log_linear_model.fit(X, merged_df['Log_Total_Sightings'])
            predictions_log_linear = np.exp(log_linear_model.predict(X))
            metrics['log-linear']['r2'].append(r2_score(y, predictions_log_linear))
            metrics['log-linear']['rmse'].append(mean_squared_error(y, predictions_log_linear, squared=False))

            # Log-Polynomial Regression
            merged_df['Log_Total_Sightings'] = np.log(merged_df['Total_Sightings'])
            X_poly_log = poly.fit_transform(X)
            log_polynomial_model = LinearRegression()
            log_polynomial_model.fit(X_poly_log, merged_df['Log_Total_Sightings'])
            predictions_log_poly = np.exp(log_polynomial_model.predict(X_poly_log))
            metrics['log-polynomial']['r2'].append(r2_score(y, predictions_log_poly))
            metrics['log-polynomial']['rmse'].append(mean_squared_error(y, predictions_log_poly, squared=False))

            # Random Forest Regression
            rf_model = RandomForestRegressor(n_estimators=100)
            rf_model.fit(X, y)
            predictions_rf = rf_model.predict(X)
            metrics['random-forest']['r2'].append(r2_score(y, predictions_rf))
            metrics['random-forest']['rmse'].append(mean_squared_error(y, predictions_rf, squared=False))

            # Write results for the current year to the file
            results_file.write(f"Year: {year}\n")
            for method, metric in metrics.items():
                results_file.write(f"{method} - R²: {np.mean(metric['r2']):.4f}, RMSE: {np.mean(metric['rmse']):.4f}\n")
            results_file.write("\n")
            
            # Plotting only raw x and y values
            plt.figure(figsize=(10, 6))
            plt.scatter(X, y, color='blue', label='Actual Data')

            plt.title(f'Scatter Plot of Total Sightings vs. Pesticide Usage for {year}')
            plt.xlabel('Pesticide Usage (ppm)')
            plt.ylabel('Total Sightings')
            plt.legend()
            plt.savefig(f'plots/scatter_plot_{year}.png')
            plt.close()
            
        else:
            results_file.write(f"Year: {year}, Not enough data for analysis.\n\n")
            # Leave None for this year in the totals

    # Create a DataFrame for aggregated results
    aggregated_data = pd.DataFrame({
        'Year': years_to_analyze,
        'Total_Sightings': total_sightings_by_year,
        'Total_Usage': total_usage_by_year
    })

    # Plotting the aggregated data
    plt.figure(figsize=(10, 6))
    plt.scatter(aggregated_data['Total_Usage'], aggregated_data['Total_Sightings'], color='blue')
    plt.title('Total Monarch Sightings vs. Total Pesticide Usage (1997-2022)')
    plt.xlabel('Total Pesticide Usage (ppm)')
    plt.ylabel('Total Monarch Sightings')
    plt.grid(True)
    plt.savefig('plots/aggregated_scatter_plot.png')
    plt.close()

    # Report average metrics across years for each method
    results_file.write("\nAverage Metrics from 1997 to 2022:\n")
    for method, metric in metrics.items():
        average_r2 = np.mean(metric['r2']) if metric['r2'] else None
        average_rmse = np.mean(metric['rmse']) if metric['rmse'] else None
        results_file.write(f"{method} - Average R²: {average_r2:.4f}, Average RMSE: {average_rmse:.4f}\n")

# Print the average results to the console
for method, metric in metrics.items():
    average_r2 = np.mean(metric['r2']) if metric['r2'] else None
    average_rmse = np.mean(metric['rmse']) if metric['rmse'] else None
    print(f"{method} - Average R²: {average_r2:.4f}, Average RMSE: {average_rmse:.4f}")
