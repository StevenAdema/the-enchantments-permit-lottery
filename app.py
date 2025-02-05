from flask import Flask, render_template, request
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Path to CSV file (adjust if needed)
CSV_PATH = os.path.join(os.path.dirname(__file__), 'data', '2025_lottery.csv')

# Load CSV into a dictionary for quick lookup:
# data_lookup[(date, zone)] = probability
def load_data(csv_path=CSV_PATH):
    data_lookup = {}
    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['application_date'], row['zone'])
            try:
                data_lookup[key] = float(row['percentage_awarded'])
            except (ValueError, KeyError):
                data_lookup[key] = 100.0
    return data_lookup

data_lookup = load_data()

def validate_input(date_zone_list):
    return True, ""  # Placeholder for now
    # Ensure 3 unique combos and date within May–Oct 2025
    # Return (is_valid, error_message)
    unique_set = set()
    for date_str, zone_str in date_zone_list:
        # Basic uniqueness check
        combo = (date_str, zone_str)
        if combo in unique_set:
            return False, f"Duplicate combination: {date_str} + {zone_str}"
        unique_set.add(combo)
        # Basic date-range check
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            if not (date_obj.year == 2025 and 5 <= date_obj.month <= 10):
                return False, f"Date out of range: {date_str}"
        except ValueError:
            return False, f"Invalid date format: {date_str}"
        # ...

    return True, ""

def calculate_probability(date_zone_list):
    # Probability of "at least one" success = 
    # 1 - Π(1 - P(each selection))
    # P is in percentages in CSV
    total_probability = 1.0
    individual_probabilities = []
    for date_str, zone_str in date_zone_list:
        p = data_lookup.get((date_str, zone_str), 0.0) / 100.0
        individual_probabilities.append(p * 100)  # Store as percentage
        total_probability *= (1 - p)
    total_probability_percentage = round((1 - total_probability) * 100, 2)  # Return as percentage
    return total_probability_percentage, individual_probabilities

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = ""
    total_probability = 0.0
    individual_probabilities = [0.3, 0.7, 3.1]  # Initialize with default values
    # Pre-populate or store user selections
    selected_combos = [("", ""), ("", ""), ("", "")]

    if request.method == 'POST':
        # Retrieve combos from form
        date1 = request.form.get('date1')
        zone1 = request.form.get('zone1')
        date2 = request.form.get('date2')
        zone2 = request.form.get('zone2')
        date3 = request.form.get('date3')
        zone3 = request.form.get('zone3')

        selected_combos = [
            (date1, zone1),
            (date2, zone2),
            (date3, zone3)
        ]

        # Validate
        valid, error_message = validate_input(selected_combos)
        if valid:
            total_probability, individual_probabilities = calculate_probability(selected_combos)
        else:
            print('Validation failed:', error_message)

    return render_template(
        'index.html',
        error_message=error_message,
        total_probability=total_probability,
        selected_combos=selected_combos,
        individual_probabilities=individual_probabilities
    )

if __name__ == '__main__':
    app.run(debug=True)