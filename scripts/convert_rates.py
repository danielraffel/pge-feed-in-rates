import csv
import json
import datetime
import os

def csv_to_json(csv_file_path, json_file_path):
    """
    Convert a CSV file with utility rates to JSON format for EVCC feed-in rates.
    
    Args:
        csv_file_path: Path to the input CSV file
        json_file_path: Path to save the output JSON file
    """
    # List to store the converted data
    json_data = []
    
    # Open and read the CSV file
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            # Parse the date and time
            date_start = row['DateStart']
            time_start = row['TimeStart']
            
            # Parse MM/DD/YYYY format
            month, day, year = map(int, date_start.split('/'))
            
            # Parse HH:MM:SS format
            hour, minute, second = map(int, time_start.split(':'))
            
            # Create datetime object in UTC
            start_datetime = datetime.datetime(year, month, day, hour, minute, second, tzinfo=datetime.timezone.utc)
            
            # Create end datetime (1 hour after start)
            end_datetime = start_datetime + datetime.timedelta(hours=1)
            
            # Format the datetime strings
            start_str = start_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
            end_str = end_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
            
            # Get the price (assuming 'Value' is the price column)
            try:
                price = float(row['Value'])
            except (ValueError, KeyError):
                print(f"Warning: Could not parse price for row: {row}")
                continue
            
            # Create the entry
            entry = {
                'start': start_str,
                'end': end_str,
                'price': price
            }
            
            json_data.append(entry)
    
    # Sort the data by start time
    json_data.sort(key=lambda x: x['start'])
    
    # Write to JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)
    
    print(f"Successfully converted {len(json_data)} entries to JSON format.")
    print(f"JSON file saved to: {os.path.abspath(json_file_path)}")

if __name__ == "__main__":
    # Get the path to the CSV file
    csv_file = "2025.csv"  # Assuming the file is in the current directory
    json_file = "feed-in-rates.json"
    
    # Verify the CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: Could not find CSV file: {csv_file}")
        print("Make sure '2025.csv' is in the current directory.")
        exit(1)
    
    # Convert CSV to JSON
    csv_to_json(csv_file, json_file)
