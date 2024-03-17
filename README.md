
# Past Performance Book Tool

## Overview

The 'Past Performance Book Tool' was crafted to simplify the intricacies of sports betting by providing a user-friendly interface. This versatile model covers NFL, NBA, NHL, and WNBA, making the analysis of each team's historical performance effortless. By running the application, users can conveniently access and visualize the projected outcomes for all games scheduled on a given day.

## Table of Contents

- Installation
- Usage
- Data
- Dependencies
- Contributing
- License
- Note from Matthew

## Installation

1. Unzip the folder from the compressed .ZIP file onto your computer, placing it in a location of your choice.

2. Navigate to python.org, access the Downloads section, choose your operating system, download the installer, execute it, and adhere to the prompts on your screen.

3. After Python has been successfully installed, return to the folder, right-click to open the terminal at the folder location. Execute the command `pip install -r requirements.txt`, and your setup will be complete!

### Get API Key

1. **Get The Odds API Key**
   - Navigate to [https://the-odds-api.com/#get-access](https://the-odds-api.com/#get-access).
   - Click the "Get API Key" button and create an account (it's 100% free).
   - Follow the website's instructions to acquire your API key.

2. **Locate .JSON File**
   - Find the ‘api-key_the-odds-api.json’ file and paste your API key within.

*Main Folder -> Your Sport -> api_keys -> api-key_the-odds-api.json*

3. **Update API Key File**
   - Open the file named 'api-key_the-odds-api.json' with a text editor (e.g., vscode).
   - Paste your API key into the file. Your file should look like this:

```json
{
   "api_key": "PASTE KEY HERE"
}
```

## Usage

1. Open the folder corresponding to the professional sports league you want to analyze, set lines for, or obtain estimates about. Locate the file named "main.py" within the folder and execute the program. It may be necessary to run the program as an administrator, though in most cases, it is not required.

2. After launching the program, allow it to complete its process. It will gather information from the internet, including odds, past performances, and historical data. This process may take a few minutes, but it is entirely normal.

3. The file labeled 'container.xlsx' will automatically open, presenting your generated predictions.


## Data

Data on odds is gathered from the free API, the-odds-api.com. The odds and name information is subsequently transferred to the respective 'odds.csv' files. Past performance data is scraped from basketball-reference.com, pro-football-reference.com, and hockey-reference.com, and this information is exported to the corresponding 'pp.csv' files. Following data collection, it undergoes processing through data cleaning procedures and is then selectively imported into the 'container.xlsx' file specific to your chosen league. The container file performs all necessary calculations and compiles the results.

## Dependencies

- csv
- datetime
- json
- os
- pathlib
- StringIO
- sys
- time
- BeautifulSoup==4.12.2
- openpyxl==3.1.2
- pandas==2.1.0
- pytz==2023.3.post1
- requests==2.31.0
- lxml==5.1.0

## Contributing

Thank you for considering contributing to the Past Performance Book Tool! Contributions are highly encouraged!

## License

This sports prediction model is released under the GNU General Public License version 2 (GPL-2.0).

You can find a copy of the license in the LICENSE.docx file included with this distribution.

## Note From Matthew

As the 'Past Performance Book Tool' is entirely open-source—a concept that has come to fruition—utilizing the program is straightforward and basic. The choice is yours whether you wish to introduce your own modifications or contribute updates and ideas to enhance and enrich the project. If you choose to do so, please let me know! I’m interested in seeing your upgrades. Enjoy and be safe!
