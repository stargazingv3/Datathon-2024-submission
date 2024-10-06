import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

# Base URL of the website
base_url = "https://journeynorth.org/sightings/querylist.html"

# List of years and seasons to scrape
years = list(range(1997, 2023))  # 1997 to 2022
seasons = ['fall', 'spring']

# Create a directory to store individual CSV files
output_dir = 'Data'
os.makedirs(output_dir, exist_ok=True)

# Iterate through each year and season
for year in years:
    # Open a CSV file to write the data for the current year
    year_file_path = os.path.join(output_dir, f'monarch-adult-{year}.csv')
    
    with open(year_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # Write the header row
        headers = ['Month', 'Year', 'Town', 'State', 'Latitude', 'Longitude', 'Number']
        writer.writerow(headers)

        # Process each season
        for season in seasons:
            # Construct the URL for each season and year
            url = f"{base_url}?season={season}&map=monarch-adult-{season}&year={year}&submit=View+Data"
            
            # Send a GET request to the website
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find the table on the page
                table = soup.find('table')

                # If the table exists, proceed
                if table:
                    # Write the data rows
                    for row in table.find_all('tr')[1:]:  # Skip the header row
                        cols = row.find_all('td')
                        if len(cols) < 7:  # Ensure there are enough columns
                            continue

                        # Extract relevant data
                        date_str = cols[1].text.strip()  # Date
                        town = cols[2].text.strip()       # Town
                        state = cols[3].text.strip()      # State
                        latitude = cols[4].text.strip()   # Latitude
                        longitude = cols[5].text.strip()  # Longitude
                        number = cols[6].text.strip()     # Number

                        # Parse the date to get month and year
                        try:
                            date_obj = datetime.strptime(date_str, '%m/%d/%y')
                            month = date_obj.month
                            year = date_obj.year
                        except ValueError:
                            continue  # Skip rows with invalid date formats

                        # Write the extracted data to the CSV
                        writer.writerow([month, year, town, state, latitude, longitude, number])

                else:
                    print(f"No table found for {season} {year}.")
            else:
                print(f"Failed to retrieve data for {season} {year}: {response.status_code}")

    print(f"Data for the year {year} has been written to '{year_file_path}'.")

print("All data has been processed and written to individual CSV files.")
