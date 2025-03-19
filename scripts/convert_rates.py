import csv
import json
import datetime
import os
import re
import glob
from collections import defaultdict

def extract_vintage_year(filename):
    """
    Extract the vintage year from the filename.
    
    Args:
        filename: The name of the file
    
    Returns:
        The vintage year as a string, or None if not found
    """
    # Look for a pattern like "2023 Vintage" or similar in the filename
    match = re.search(r'20(\d{2})\s*Vintage', filename)
    if match:
        return match.group(1)  # Return just the last 2 digits
    
    # Fallback to any 4-digit year
    match = re.search(r'20(\d{2})', filename)
    if match:
        return match.group(1)  # Return just the last 2 digits
    
    return None

def process_csv_row(row):
    """
    Process a single CSV row and convert it to the required JSON format.
    
    Args:
        row: Dictionary containing CSV row data
    
    Returns:
        Tuple containing:
        - entry: Dictionary in the required JSON format
        - year: The calendar year from the date
        - time_key: A unique key for this time slot
        - rate_type: String indicating "generation" or "delivery"
    """
    try:
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
        
        # Get the price
        price = float(row['Value'])
        
        # Create the entry
        entry = {
            'start': start_str,
            'end': end_str,
            'price': price
        }
        
        # Create a unique key for this time slot
        time_key = f"{start_str}_{end_str}"
        
        # Determine rate type based on the RIN field
        # Default to delivery for safety
        rate_type = "delivery"
        
        # Check all keys to find the one with RIN (handling BOM issues)
        rin_value = None
        for key in row.keys():
            # Strip BOM characters and whitespace
            clean_key = key.strip().replace('\ufeff', '')
            if clean_key == 'RIN':
                rin_value = row[key]
                break
        
        # If found, determine the rate type
        if rin_value:
            if 'USCA-XXPG' in rin_value:
                rate_type = "generation"
            elif 'USCA-PGXX' in rin_value:
                rate_type = "delivery"
        
        return entry, year, time_key, rate_type
    except (ValueError, KeyError) as e:
        print(f"Warning: Could not parse row: {row}. Error: {e}")
        return None, None, None, None

def csv_to_json(csv_file_path, output_dir=None):
    """
    Convert a CSV file with utility rates to JSON format for EVCC feed-in rates.
    Create separate files for generation and delivery rates.
    
    Args:
        csv_file_path: Path to the input CSV file
        output_dir: Directory to save the output JSON files (default: current directory)
    """
    # Extract the vintage year from the filename
    base_filename = os.path.basename(csv_file_path)
    vintage_year = extract_vintage_year(base_filename)
    
    if not vintage_year:
        print(f"Warning: Could not extract vintage year from filename: {base_filename}")
        vintage_year = "unknown"
    else:
        print(f"Processing {base_filename} (Vintage: NBT{vintage_year})...")
    
    # Dictionaries to store generation and delivery rates by year
    generation_data = defaultdict(dict)  # {year: {time_key: entry}}
    delivery_data = defaultdict(dict)    # {year: {time_key: entry}}
    
    # For debugging, capture raw data
    raw_data = []
    
    # Open and read the CSV file, handling BOM
    with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
        # Read the first line to get the true header (without BOM)
        header_line = csv_file.readline().strip()
        headers = header_line.split(',')
        
        # Reset file pointer to the beginning
        csv_file.seek(0)
        
        csv_reader = csv.DictReader(csv_file)
        generation_count = 0
        delivery_count = 0
        row_count = 0
        
        for row in csv_reader:
            row_count += 1
            
            # Collect raw data for debugging
            if row_count <= 5:
                raw_data.append(row)
            
            entry, entry_year, time_key, rate_type = process_csv_row(row)
            
            if entry and time_key and entry_year and rate_type:
                # Only store data for years 2025 to 2033
                if 2025 <= entry_year <= 2033:
                    # Store in the appropriate dictionary based on rate type
                    if rate_type == "generation":
                        generation_data[entry_year][time_key] = entry
                        generation_count += 1
                    else:  # delivery
                        delivery_data[entry_year][time_key] = entry
                        delivery_count += 1
        
        print(f"Processed {row_count} rows: {generation_count} generation rates, {delivery_count} delivery rates")
    
    # Debug - print raw data
    print("DEBUG: Raw data inspection:")
    for i, row in enumerate(raw_data):
        print(f"Row {i+1} keys: {', '.join(row.keys())}")
        print(f"Row {i+1} values: {', '.join(str(v) for v in row.values())}")
        
        # Try to find the RIN field regardless of BOM issues
        rin_key = None
        rin_value = None
        for key, value in row.items():
            if key.strip().replace('\ufeff', '') == 'RIN':
                rin_key = key
                rin_value = value
                break
        
        print(f"Row {i+1} RIN key: {rin_key}")
        print(f"Row {i+1} RIN value: {rin_value}")
    
    # Debug: Rate type distribution
    print(f"DEBUG: Rate type distribution:")
    for year in sorted(set(list(generation_data.keys()) + list(delivery_data.keys()))):
        gen_count = len(generation_data[year]) if year in generation_data else 0
        del_count = len(delivery_data[year]) if year in delivery_data else 0
        print(f"  Year {year}: {gen_count} generation rates, {del_count} delivery rates")
    
    # Create the comprehensive JSON files for all years
    
    # 1. Generation rates file - only if we have generation data
    all_generation_entries = []
    for year_entries in generation_data.values():
        all_generation_entries.extend(year_entries.values())
    
    if all_generation_entries:
        all_generation_entries.sort(key=lambda x: x['start'])
        gen_file = f"NBT{vintage_year}-generation-feed-in-rates.json"
        if output_dir:
            gen_file = os.path.join(output_dir, gen_file)
        
        with open(gen_file, 'w') as json_file:
            json.dump(all_generation_entries, json_file, indent=2)
        
        print(f"Comprehensive generation file saved to: {os.path.abspath(gen_file)} ({len(all_generation_entries)} entries)")
    
    # 2. Delivery rates file - only if we have delivery data
    all_delivery_entries = []
    for year_entries in delivery_data.values():
        all_delivery_entries.extend(year_entries.values())
    
    if all_delivery_entries:
        all_delivery_entries.sort(key=lambda x: x['start'])
        del_file = f"NBT{vintage_year}-delivery-feed-in-rates.json"
        if output_dir:
            del_file = os.path.join(output_dir, del_file)
        
        with open(del_file, 'w') as json_file:
            json.dump(all_delivery_entries, json_file, indent=2)
        
        print(f"Comprehensive delivery file saved to: {os.path.abspath(del_file)} ({len(all_delivery_entries)} entries)")
    
    # Create yearly folders and separate JSON files for generation and delivery rates
    # Process each year
    for year in sorted(set(list(generation_data.keys()) + list(delivery_data.keys()))):
        # Create year-specific directory
        year_dir = os.path.join(output_dir if output_dir else "", str(year))
        if not os.path.exists(year_dir):
            os.makedirs(year_dir)
        
        # 1. Generation rates file for this year - only if we have generation data
        if year in generation_data and generation_data[year]:
            year_gen_entries = list(generation_data[year].values())
            year_gen_entries.sort(key=lambda x: x['start'])
            
            year_gen_file = os.path.join(year_dir, f"NBT{vintage_year}-generation-feed-in-rates.json")
            
            with open(year_gen_file, 'w') as json_file:
                json.dump(year_gen_entries, json_file, indent=2)
            
            print(f"Year {year} generation file saved to: {os.path.abspath(year_gen_file)} ({len(year_gen_entries)} entries)")
        
        # 2. Delivery rates file for this year - only if we have delivery data
        if year in delivery_data and delivery_data[year]:
            year_del_entries = list(delivery_data[year].values())
            year_del_entries.sort(key=lambda x: x['start'])
            
            year_del_file = os.path.join(year_dir, f"NBT{vintage_year}-delivery-feed-in-rates.json")
            
            with open(year_del_file, 'w') as json_file:
                json.dump(year_del_entries, json_file, indent=2)
            
            print(f"Year {year} delivery file saved to: {os.path.abspath(year_del_file)} ({len(year_del_entries)} entries)")

def process_all_csv_files():
    """
    Process all PG&E NBT EEC Values CSV files in the current directory.
    """
    # Create 'output' directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Find all CSV files that match the pattern
    csv_files = glob.glob("*PG&E*NBT*EEC*Values*Vintage*.csv")
    
    # Also include the specific file format for testing
    year_pattern_files = glob.glob("20??.csv")
    
    # Combine and remove duplicates
    all_csv_files = list(set(csv_files + year_pattern_files))
    
    if not all_csv_files:
        print("No matching CSV files found.")
        print("Looking for files matching patterns: '*PG&E*NBT*EEC*Values*Vintage*.csv' or '20??.csv'")
        return
    
    print(f"Found {len(all_csv_files)} CSV files to process.")
    
    # Process each CSV file
    for csv_file in all_csv_files:
        csv_to_json(csv_file, output_dir)

if __name__ == "__main__":
    process_all_csv_files()
