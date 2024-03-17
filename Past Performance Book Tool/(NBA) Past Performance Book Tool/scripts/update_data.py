import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from pathlib import Path
from io import StringIO
import time

# Function to clean the DataFrame
def clean_data(year_data, year):
    # Remove duplicate header rows
    year_data = year_data[~year_data.eq(year_data.iloc[0]).all(1)]

    # Remove rows with 4 or more empty cells side by side
    year_data = year_data.dropna(thresh=year_data.shape[1] - 3)

    # Remove columns with headers containing "Unnamed"
    year_data = year_data.loc[:, ~year_data.columns.str.contains('^Unnamed')]

    # Remove columns with headers containing "Notes"
    year_data = year_data.loc[:, ~year_data.columns.str.contains('Notes')]

    year_data['Year'] = year

    return year_data

# Get the current date
current_date = datetime.now()
current_year = current_date.year
current_month = current_date.month

# Define the number of recent years to scrape (2 years)
num_years = 2

# Define the list of months to scrape
months_to_scrape = ['october', 'november', 'december', 'january', 'february', 'march', 'april']

# Determine the target year based on the current date
if current_month < 11:
    # If it's before November in the current year, scrape the previous num_years years
    years_to_scrape = [current_year - i for i in range(num_years)]
else:
    # If it's November or later, scrape the current year and the previous (num_years - 1) years
    years_to_scrape = [current_year+1] + [current_year+1 - i for i in range(1, num_years)]

# Reverse the list to scrape from oldest to newest
years_to_scrape.reverse()

# Create an empty DataFrame to store the scraped data
data = pd.DataFrame()

# Determine the script's directory
script_directory = Path(__file__).resolve().parent

for year in years_to_scrape:
    for month in months_to_scrape:
        # Create the URL for the current year and month
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html"

        # Send an HTTP GET request to the URL
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Parse the HTML content and continue with web scraping as before
            soup = BeautifulSoup(response.text, "html.parser")

            games_table = soup.find("table", {"id": "schedule"})

            if games_table:
                print(f"Scraping data for year: {year}, month: {month}")
                # Extract the table data into a DataFrame using StringIO
                year_data = pd.read_html(StringIO(str(games_table)))[0]

                # Clean the data using the function
                year_data = clean_data(year_data, year)

                data = pd.concat([data, year_data], ignore_index=True)
            else:
                print(f"Table 'games' not found for year {year}, month {month}.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve the page for year {year}, month {month}. Exception:", e)

        # Add a 5-second delay before the next request
        time.sleep(3)

# Save the cleaned data to a CSV file in the 'data' directory related to the script's location
csv_filename = "pp.csv"
csv_file_path = script_directory / ".." / "data" / csv_filename

# Use mode='w' to overwrite the existing file
data.to_csv(csv_file_path, index=False, mode='w')

print("Completed")
