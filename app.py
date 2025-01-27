from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

# Path to CSV file (adjust if needed)
CSV_PATH = os.path.join(os.path.dirname(__file__), 'data', 'data.csv')

# Load CSV into a dictionary for quick lookup:
# data_lookup[(date, zone)] = probability
def load_data(csv_path=CSV_PATH):
    data_lookup = {}
    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['application_date'], row['zone'])
            data_lookup[key] = float(row['precentage_awarded'])
    return data_lookup

data_lookup = load_data()

def validate_input(date_zone_list):
    # Ensure 3 unique combos and date within May–Oct 2025
    # Return (is_valid, error_message)
    unique_set = set()
    for date_str, zone_str in date_zone_list:
        # Basic uniqueness check
        combo = (date_str, zone_str)
        if combo in unique_set:
            return False, f"Duplicate combination: {date_str} + {zone_str}"
        unique_set.add(combo)

        # Basic date-range check (placeholder - actual validation can parse date)
        # E.g., "YYYY-MM-DD" format or "MM-DD" with a year check
        # If not valid, return (False, "Invalid date")
        # ...

    return True, ""

def calculate_probability(date_zone_list):
    # Probability of "at least one" success = 
    # 1 - Π(1 - P(each selection))
    # P is in percentages in CSV
    total_probability = 1.0
    for date_str, zone_str in date_zone_list:
        p = data_lookup.get((date_str, zone_str), 0.0) / 100.0
        total_probability *= (1 - p)
    return round((1 - total_probability) * 100, 2)  # Return as percentage

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = ""
    total_probability = 0.0
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
            total_probability = calculate_probability(selected_combos)

    return render_template(
        'index.html',
        error_message=error_message,
        total_probability=total_probability,
        selected_combos=selected_combos
    )

if __name__ == '__main__':
    app.run(debug=True)