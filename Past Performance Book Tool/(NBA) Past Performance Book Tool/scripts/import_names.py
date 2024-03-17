import pandas as pd
import os
import openpyxl as px
from datetime import datetime, timedelta

# Define constants
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'odds.csv')
EXCEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'container.xlsx')

def read_csv_data(csv_file):
    try:
        return pd.read_csv(csv_file, encoding='ISO-8859-1')
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {csv_file}")

def extract_team_commence_data(dataframe):
    team_data = {}
    current_date = datetime.now()
    for index, row in dataframe.iterrows():
        away_team = row['away_team']
        home_team = row['home_team']
        commence_date = datetime.strptime(row['commence_date'], "%m/%d/%Y")
        commence_hour = datetime.strptime(row['commence_hour'], "%I:%M %p")
        
        
        if away_team not in team_data:
            if commence_date - current_date <= timedelta(days=0):
                team_data[away_team] = (commence_date.strftime("%m/%d/%Y"), commence_hour.strftime("%I:%M %p"))
        if home_team not in team_data:
            if commence_date - current_date <= timedelta(days=0):
                team_data[home_team] = (commence_date.strftime("%m/%d/%Y"), commence_hour.strftime("%I:%M %p"))
    
    return team_data

def write_data_to_excel(excel_file, team_data):
    book = px.load_workbook(excel_file)
    sheet = book.active

    # Clear existing data in the 'Date' and 'Time' columns
    for cell in sheet['D'][1:]:
        cell.value = None
    for cell in sheet['A'][1:]:
        cell.value = None
    for cell in sheet['B'][1:]:
        cell.value = None

    # Write new data to columns 'Date' and 'Time'
    for i, (team_name, (commence_date, commence_hour)) in enumerate(team_data.items(), start=2):
        sheet[f'D{i}'] = team_name
        sheet[f'A{i}'] = commence_date
        sheet[f'B{i}'] = commence_hour

    book.save(excel_file)

if __name__ == '__main__':
    try:
        data = read_csv_data(CSV_PATH)
        team_data = extract_team_commence_data(data)
        write_data_to_excel(EXCEL_PATH, team_data)
        print("Completed")
    except FileNotFoundError as e:
        print(e)
