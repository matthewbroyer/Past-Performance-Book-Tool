import os
import subprocess

def run_script(script_file, success_messages):
    script_path = os.path.join(scripts_folder, script_file)
    try:
        completed_process = subprocess.run(['python', script_path], check=True, capture_output=True, text=True)
        if completed_process.returncode == 0:
            print(success_messages.get(script_file, f"Successfully ran {script_file}"))
        else:
            print(f"Error while running {script_file}")
    except Exception as e:
        print(f"Error while running {script_file}: {e}")

# Get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate to the 'scripts' folder
scripts_folder = os.path.join(current_script_dir, 'scripts')

# List of scripts to run
scripts_to_run = ['update_odds.py', 'update_data.py', 'import_names.py', 'import_scores.py', 'import_scores_h2h.py']

# Map script names to desired success messages
success_messages = {
    'update_odds.py': 'Odds Table: Updated\nFetching data...',
    'update_data.py': 'Data: Fetched',
    'import_names.py': 'Dates: Imported\nTimes: Imported\nTeam Names: Imported',
    'import_scores.py': 'Calculations: Complete',
    'import_scores_h2h.py': 'Calculations: Complete'
}

# Run each specified script in the 'scripts' folder
for script_file in scripts_to_run:
    run_script(script_file, success_messages)

# Open the "container.xlsx" file
xlsx_file_path = os.path.join(current_script_dir, 'container.xlsx')
if os.name == 'nt':  # Windows
    os.startfile(xlsx_file_path)
else:
    subprocess.Popen(['open', xlsx_file_path])  # For non-Windows platforms
