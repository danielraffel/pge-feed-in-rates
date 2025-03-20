import csv
import json
import datetime
import os
import re
import glob
import zipfile
import tempfile
from collections import defaultdict

def extract_vintage_year(filename):
    """
    Extract the vintage year from the filename.
    
    Args:
        filename: The name of the file
    
    Returns:
        The vintage year as a string, or "00" for floating vintage, or None if not found
    """
    # Check for Floating Vintage files
    if "Floating Vintage" in filename:
        return "00"
    
    # Look for a pattern like "NBT23" or "NBT 23" in the filename
    match = re.search(r'NBT\s*(\d{2})', filename, re.IGNORECASE)
    if match:
        return match.group(1)
    
    # Look for a pattern like "2023 Vintage" or similar in the filename
    match = re.search(r'20(\d{2})\s*Vintage', filename)
    if match:
        return match.group(1)  # Return just the last 2 digits
    
    # Fallback to any 4-digit year
    match = re.search(r'20(\d{2})', filename)
    if match:
        return match.group(1)  # Return just the last 2 digits
    
    return None

def get_vintage_year_range(vintage_year, current_year=None):
    """
    Determine the year range for a specific vintage.
    
    Args:
        vintage_year: The vintage year as a string (e.g., "23" for NBT23)
        current_year: The current year (default: current system year)
    
    Returns:
        Tuple containing start_year and end_year
    """
    if current_year is None:
        current_year = datetime.datetime.now().year
    
    # Mapping of known vintage years to their ranges
    vintage_ranges = {
        "00": (2025, 2026),  # NBT00 (Floating Vintage) - only 2 years
        "23": (2023, 2031),  # NBT23 - 9 years
        "24": (2024, 2032),  # NBT24 - 9 years
        "25": (2025, 2033),  # NBT25 - 9 years
        "26": (2026, 2034),  # NBT26 - 9 years
    }
    
    # Check if we have a predefined range for this vintage
    if vintage_year in vintage_ranges:
        return vintage_ranges[vintage_year]
    
    # For unknown or future vintages, use a default 9-year period
    # starting from the vintage year (if it's numeric)
    try:
        vintage_num = int(vintage_year)
        start_year = 2000 + vintage_num
        end_year = start_year + 8  # 9 years total (including start year)
        return (start_year, end_year)
    except ValueError:
        # Fallback to a default range if vintage year is not numeric
        return (2025, 2033)

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
    
    # Determine the year range based on vintage
    current_year = datetime.datetime.now().year
    start_year, end_year = get_vintage_year_range(vintage_year, current_year)
    
    print(f"Generating data for years {start_year} to {end_year}")
    
    # Create "archives" directory to store comprehensive files
    archives_dir = os.path.join(output_dir if output_dir else "", "archives")
    if not os.path.exists(archives_dir):
        os.makedirs(archives_dir)
    
    # Dictionaries to store generation and delivery rates by year
    generation_data = defaultdict(dict)  # {year: {time_key: entry}}
    delivery_data = defaultdict(dict)    # {year: {time_key: entry}}
    
    # For debugging, capture raw data (limiting to avoid memory issues with large files)
    raw_data = []
    
    try:
        # First pass - check the file size to determine if we should use chunked processing
        file_size = os.path.getsize(csv_file_path)
        large_file = file_size > 100 * 1024 * 1024  # 100MB threshold
        
        if large_file:
            print(f"Large file detected ({file_size / (1024*1024):.2f} MB). Using memory-efficient processing...")
        
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
                
                # Collect a sample of raw data for debugging (limit to 5 rows)
                if row_count <= 5:
                    raw_data.append(row)
                
                entry, entry_year, time_key, rate_type = process_csv_row(row)
                
                if entry and time_key and entry_year and rate_type:
                    # Only store data for years within our range
                    if start_year <= entry_year <= end_year:
                        if rate_type == "generation":
                            generation_data[entry_year][time_key] = entry
                            generation_count += 1
                        else:  # delivery
                            delivery_data[entry_year][time_key] = entry
                            delivery_count += 1
                
                # Progress indicator for large files
                if large_file and row_count % 100000 == 0:
                    print(f"  Processed {row_count} rows so far...")
            
            print(f"Processed {row_count} rows: {generation_count} generation rates, {delivery_count} delivery rates for years {start_year}-{end_year}")
        
        # Debug - print raw data samples
        print("DEBUG: Raw data inspection (sample):")
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
            
    except Exception as e:
        print(f"Error processing CSV file {csv_file_path}: {e}")
        import traceback
        traceback.print_exc()
    
    # Create the comprehensive JSON files for all years - store in archives folder
    
    # 1. Generation rates file - only if we have generation data
    all_generation_entries = []
    for year_entries in generation_data.values():
        all_generation_entries.extend(year_entries.values())
    
    if all_generation_entries:
        all_generation_entries.sort(key=lambda x: x['start'])
        gen_file = f"NBT{vintage_year}-generation-feed-in-rates.json"
        gen_file = os.path.join(archives_dir, gen_file)
        
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
        del_file = os.path.join(archives_dir, del_file)
        
        with open(del_file, 'w') as json_file:
            json.dump(all_delivery_entries, json_file, indent=2)
        
        print(f"Comprehensive delivery file saved to: {os.path.abspath(del_file)} ({len(all_delivery_entries)} entries)")
    
    # Create yearly folders and separate JSON files for generation and delivery rates
    # Process each year within our range
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

def extract_from_zip(zip_file_path, temp_dir):
    """
    Extract CSV file from a zip archive to a temporary directory.
    
    Args:
        zip_file_path: Path to the zip file
        temp_dir: Directory to extract the file to
    
    Returns:
        Path to the extracted CSV file or None if not found
    """
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # Find CSV files in the archive
            csv_files = [f for f in zip_ref.namelist() if f.lower().endswith('.csv')]
            
            if not csv_files:
                print(f"No CSV files found in zip archive: {zip_file_path}")
                return None
            
            # Extract all CSV files to the temp directory
            for csv_file in csv_files:
                zip_ref.extract(csv_file, temp_dir)
                extracted_path = os.path.join(temp_dir, csv_file)
                print(f"Extracted {csv_file} from {zip_file_path}")
                return extracted_path  # Return the path to the first extracted CSV
                
    except zipfile.BadZipFile:
        print(f"Error: {zip_file_path} is not a valid zip file")
    except Exception as e:
        print(f"Error extracting from {zip_file_path}: {e}")
    
    return None

def find_csv_files():
    """
    Find all PG&E NBT EEC Values CSV files in the current directory,
    including those in zip archives.
    
    Returns:
        List of file paths and their source type (zip or regular)
    """
    # Find all CSV files that match the pattern
    csv_files = glob.glob("*PG&E*NBT*EEC*Values*Vintage*.csv")
    floating_vintage_files = glob.glob("*PG&E*NBT*EEC*Values*Floating*Vintage*.csv")
    year_pattern_files = glob.glob("20??.csv")
    
    # Find all ZIP files that might contain CSV files
    zip_files = glob.glob("*PG&E*NBT*EEC*Values*Vintage*.csv.zip")
    floating_vintage_zip_files = glob.glob("*PG&E*NBT*EEC*Values*Floating*Vintage*.csv.zip")
    year_pattern_zip_files = glob.glob("20??.csv.zip")
    
    # Combine all CSV files
    all_csv_files = csv_files + floating_vintage_files + year_pattern_files
    all_zip_files = zip_files + floating_vintage_zip_files + year_pattern_zip_files
    
    # Create a mapping of base filenames to their full paths
    # This helps us identify when both zipped and unzipped versions exist
    file_mapping = {}
    
    # Add regular CSV files to the mapping
    for file_path in all_csv_files:
        base_name = os.path.basename(file_path)
        file_mapping[base_name] = {'path': file_path, 'type': 'regular'}
    
    # Add zip files, prioritizing them over regular files
    for zip_path in all_zip_files:
        base_name = os.path.basename(zip_path)[:-4]  # Remove .zip extension
        file_mapping[base_name] = {'path': zip_path, 'type': 'zip'}
    
    # Convert the mapping back to a list of files with their types
    result = []
    for file_info in file_mapping.values():
        result.append(file_info)
    
    return result

def process_all_csv_files():
    """
    Process all PG&E NBT EEC Values CSV files in the current directory,
    including those in zip archives.
    """
    # Create 'output' directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Find all CSV and zip files
    all_files = find_csv_files()
    
    if not all_files:
        print("No matching CSV or ZIP files found.")
        print("Looking for files matching patterns like:")
        print("- PG&E NBT EEC Values *Vintage*.csv")
        print("- PG&E NBT EEC Values *Vintage*.csv.zip")
        print("- PG&E NBT EEC Values Floating Vintage.csv")
        print("- PG&E NBT EEC Values Floating Vintage.csv.zip")
        return
    
    print(f"Found {len(all_files)} files to process.")
    
    # Create a temporary directory for extracted files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Process each file
        for file_info in all_files:
            file_path = file_info['path']
            file_type = file_info['type']
            
            if file_type == 'zip':
                # Extract the CSV from the zip file
                extracted_path = extract_from_zip(file_path, temp_dir)
                if extracted_path:
                    print(f"Processing extracted file: {extracted_path}")
                    csv_to_json(extracted_path, output_dir)
                else:
                    print(f"Skipping zip file (no CSV found): {file_path}")
            else:
                # Process regular CSV file
                print(f"Processing regular file: {file_path}")
                csv_to_json(file_path, output_dir)

if __name__ == "__main__":
    process_all_csv_files()
