# PG&E Feed-in Rates

This repository provides PG&E feed-in rate data in JSON format for use with energy management systems like [EVCC](https://evcc.io). The data is particularly useful for PG&E solar customers who want to track their energy usage based on the rates they receive when exporting energy back to the grid.

## Repository Structure

- **Year folders (e.g., `2025/`, `2026/`, etc.)**: Contains JSON files with feed-in rates for specific calendar years
  - Example: [2025/NBT24-generation-feed-in-rates.json](2025/NBT24-generation-feed-in-rates.json)
  - Example: [2025/NBT24-delivery-feed-in-rates.json](2025/NBT24-delivery-feed-in-rates.json)

- **archives/](https://github.com/danielraffel/pge-feed-in-rates/tree/main/archives)**: Contains comprehensive JSON files with complete feed-in rates across all applicable years
  - Example: [archives/NBT24-generation-feed-in-rates.json](https://raw.githubusercontent.com/danielraffel/pge-feed-in-rates/refs/heads/main/archives/NBT24-generation-feed-in-rates.json)

- **[utility-rates/](https://github.com/danielraffel/pge-feed-in-rates/tree/main/utililty-rates)`**: Contains the original PG&E rate files and conversion script
  - Original PG&E rate files for [NBT23](https://github.com/danielraffel/pge-feed-in-rates/blob/main/utililty-rates/PG%26E%20NBT%20EEC%20Values%202023%20Vintage.csv.zip), [NBT24](https://github.com/danielraffel/pge-feed-in-rates/blob/main/utililty-rates/PG%26E%20NBT%20EEC%20Values%202024%20Vintage.csv.zip), [NBT25](https://github.com/danielraffel/pge-feed-in-rates/blob/main/utililty-rates/PG%26E%20NBT%20EEC%20Values%202025%20Vintage.csv.zip), [NBT26](https://github.com/danielraffel/pge-feed-in-rates/blob/main/utililty-rates/PG%26E%20NBT%20EEC%20Values%202026%20Vintage.csv.zip), and [NBT00](https://github.com/danielraffel/pge-feed-in-rates/blob/main/utililty-rates/PG%26E%20NBT%20EEC%20Values%20Floating%20Vintage.csv.zip) (zipped CSV format)
  - [convert-rates.py](https://github.com/danielraffel/pge-feed-in-rates/blob/main/utililty-rates/convert-rates.py): Python script to convert PG&E rate files to EVCC-compatible JSON
  - [Solar Billing Plan Export Rates Readme.txt](https://github.com/danielraffel/pge-feed-in-rates/blob/main/utililty-rates/Solar%20Billing%20Plan%20Export%20Rates%20Readme.txt): Documentation on PG&E rate files

## Understanding PG&E Feed-in Rates

PG&E's Net Billing Tariff (NBT) provides compensation for solar customers when they export energy back to the grid. Rates are determined by:

- **Vintage Year**: The year you activated your solar system (NBT23, NBT24, etc.)
- **Time of Day**, **Day Type**, and **Month**: Rates vary throughout the day, week, and year
- **Rate Type**: Generation rates vs. Delivery rates

### Vintage Years and Rate Guarantees

Per CPUC Resolution E-5301, each NBT vintage has specific guarantees:

- **NBT23, NBT24, NBT25, NBT26**: Guaranteed export rates for 9 years from Permission-To-Operate (PTO) date
- **NBT00 (Floating Vintage)**: Only rates for 2025 and 2026 are actual effective rates

Any rates beyond the guaranteed period are for illustrative purposes only and not actual effective SBP Export Rates.

### Generation vs. Delivery Rates

PG&E provides two types of feed-in rates:

- **Generation Rates** (USCA-XXPG): Compensation for the energy you generate and export
- **Delivery Rates** (USCA-PGXX): Account for the delivery component of exported energy

For most home solar customers, generation rates are typically most relevant for calculating export compensation.

## JSON File Format

The JSON files adhere to [EVCC's Custom Plugin](https://docs.evcc.io/en/docs/tariffs#dynamic-electricity-price) format:

1. **File Structure**: Each JSON file contains an array of time-price objects.
2. **Timestamp Format**: All timestamps are in Coordinated Universal Time (UTC) with the 'Z' suffix, following the ISO 8601 standard:
   * Format: `YYYY-MM-DDTHH:MM:SSZ`
   * Example: `2025-01-01T00:00:00Z`
3. **Object Structure**: Each entry contains three fields:
   * `start`: The beginning of the time period (in UTC)
   * `end`: The end of the time period (in UTC)
   * `price`: The electricity rate in dollars per kilowatt-hour
4. **Time Handling**: EVCC automatically converts the UTC timestamps to the local time zone of your installation, handling daylight saving time transitions properly.

Example:
```json
[
  { "start": "2025-01-01T00:00:00Z", "end": "2025-01-01T01:00:00Z", "price": 0.05375 },
  { "start": "2025-01-01T01:00:00Z", "end": "2025-01-01T02:00:00Z", "price": 0.04885 }
]
```

EVCC periodically checks these rates (typically once per hour) to determine the current electricity price for your feed-in calculations, allowing for accurate time-of-use pricing.

## Using with EVCC

These JSON files are formatted for [EVCC's tariff system](https://docs.evcc.io/en/docs/tariffs) for use with the [EVCC Custom Plugin](https://docs.evcc.io/en/docs/tariffs#dynamic-electricity-price). You can link to the appropriate GitHub raw file and add it to your `evcc.yaml` configuration as follows:

```yaml
tariffs:
  currency: USD
  feedin:
    type: custom
    forecast:
      source: http
      uri: https://raw.githubusercontent.com/danielraffel/pge-feed-in-rates/refs/heads/main/2025/NBT24-generation-feed-in-rates.json
```

Select the JSON file that corresponds to your solar activation year and rate type. For example, if your solar system was activated in 2024, use the NBT24-generation-feed-in-rates.json file. Adjust the year as needed—this file, for instance, retrieves 2025 rates.

## Converting Your Own Rates

This archive was last updated for **PG&E Solar Billing Plan rates offered in 2025**, and all data generated is shared in this repository. While running the script **should not be necessary** to access data circa 2025, you may want to run it with future data. 

### Things to Keep in Mind:
- The script will generate an **output folder** containing the processed files.
- It expects to be **run in the same directory** as the rate plans and it expects them to be zipped.
- If both zipped and unzipped CSV files exist, the script prioritizes processing the **zipped files**.
- It assumes the files 

### Running the Script
To convert rates for future vintage years or to re-run the conversion:

1. Navigate to the `utility-rates` directory.
2. Run the script:  
   ```bash
   python convert-rates.py
   ```

### What the Script Does:
- Generates files for each vintage according to its **appropriate year range**.
- Creates **separate JSON files** for generation and delivery rates.
- Organizes files by year and stores **comprehensive archives**.
- The script expects ZIP files, containing CSV rate plan files, to follow a specific naming convention used by PG&E. Each ZIP file includes a single CSV file inside. The expected format is:
```
• PG&E NBT EEC Values Floating Vintage.csv.zip  
• PG&E NBT EEC Values 2025 Vintage.csv.zip  
• PG&E NBT EEC Values 2026 Vintage.csv.zip  
```
This ensures the script can correctly extract and process the appropriate rate data.

### NBT Vintage Year Handling:
- **NBT00 (Floating Vintage)**: 2025-2026 only
- **NBT23**: 2023-2031 (9 years) *
- **NBT24**: 2024-2032 (9 years) *
- **NBT25**: 2025-2033 (9 years)
- **NBT26**: 2026-2034 (9 years)
- Future vintages can be easily added and mapped to appropriate **9-year periods**.

\* **Note**: NBT23 and NBT24 only generate files starting from **2025 onward**.

## About the Source Data

The original source of the PG&E data is available [here](https://www.pge.com/assets/pge/docs/vanities/PGE-Solar-Billing-Plan-Export-Rates.zip).

## Disclaimer

While every effort has been made to ensure accuracy, this repository is not officially affiliated with PG&E. Always verify rate information with PG&E for critical financial decisions.
