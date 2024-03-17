import requests
import csv
import json
import os
import sys
from datetime import datetime
from pytz import timezone

# Function to load API key from file
def load_api_key():
    api_key_file_path = os.path.join(script_dir, '..', 'api_keys', "api-key_the-odds-api.json")

    try:
        with open(api_key_file_path, "r") as api_key_file:
            api_key_data = json.load(api_key_file)
            api_key = api_key_data.get("api_key")

            if not api_key:
                raise ValueError("API key not found in api-key_the-odds-api.json")

            return api_key

    except FileNotFoundError:
        print("API key file api-key_the-odds-api.json not found in the script directory.")
        sys.exit(1)
    except ValueError as e:
        print(str(e))
        sys.exit(1)

# Function to convert UTC time to EST
def convert_utc_to_est(utc_time, date_format="%m/%d/%Y", hour_format="%I:%M %p"):
    est = timezone('US/Eastern')
    utc = timezone('UTC')
    utc_time = utc.localize(datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ"))
    est_time = utc_time.astimezone(est)
    return est_time.strftime(date_format), est_time.strftime(hour_format)

# Function to make a GET request to the API
def make_api_request(api_key):
    url = f"https://api.the-odds-api.com/v4/sports/basketball_wnba/odds?markets=h2h,spreads,totals&regions=us&oddsFormat=american&apiKey={api_key}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to retrieve data from the API. Status code:", response.status_code)
            sys.exit(1)

    except requests.RequestException as e:
        print("Error making API request:", str(e))
        sys.exit(1)

# Main function to process API response and write to CSV
def process_and_write_data(data):
    csv_file_path = os.path.join(script_dir, '..', 'data', "odds.csv")

    try:
        with open(csv_file_path, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the header row
            header = ["commence_date", "commence_hour", "home_team", "away_team", "bookmaker_key",
                      "bookmaker_title", "market_key", "outcome_name", "outcome_price", "outcome_point"]
            csv_writer.writerow(header)

            # Iterate through the data and write rows
            for item in data:
                commence_date, commence_hour = convert_utc_to_est(item["commence_time"])
                home_team = item["home_team"]
                away_team = item["away_team"]
                for bookmaker in item.get("bookmakers", []):
                    bookmaker_key = bookmaker["key"]
                    bookmaker_title = bookmaker["title"]
                    for market in bookmaker.get("markets", []):
                        market_key = market["key"]
                        for outcome in market.get("outcomes", []):
                            outcome_name = outcome["name"]
                            outcome_price = outcome.get("price", None)
                            outcome_point = outcome.get("point", None)  # Fill empty cells with "Moneyline"
                            row = [commence_date, commence_hour, home_team, away_team, bookmaker_key, bookmaker_title,
                                   market_key, outcome_name, outcome_price, outcome_point]
                            csv_writer.writerow(row)

        print("Completed")

    except IOError as e:
        print("Error writing to CSV file:", str(e))
        sys.exit(1)

# Main execution
if __name__ == "__main__":
    # Get the directory of the current script
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))

    # Extract the script's filename without the extension
    filename = os.path.splitext(os.path.basename(__file__))[0]

    # Load API key
    API_KEY = load_api_key()

    # Make API request
    api_data = make_api_request(API_KEY)

    # Process and write data to CSV
    process_and_write_data(api_data)
