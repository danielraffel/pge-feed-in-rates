# PG&E Feed-in Rates

This repository provides PG&E feed-in rate data in JSON format for use with energy management systems like [EVCC](https://evcc.io). The data is particularly useful for PG&E solar customers who want to track their energy usage based on the rates they receive when exporting energy back to the grid.

## Repository Structure

- **Year folders (e.g., [2025/](https://github.com/danielraffel/pge-feed-in-rates/tree/main/2025), [2026/](https://github.com/danielraffel/pge-feed-in-rates/tree/main/2026), etc.)**: Contains JSON files with feed-in rates for specific calendar years
  - Example: [2025/NBT24-generation-feed-in-rates.json](2025/NBT24-generation-feed-in-rates.json)
  - Example: [2025/NBT24-delivery-feed-in-rates.json](2025/NBT24-delivery-feed-in-rates.json)
  - Example: [2025/NBT24-total-feed-in-rates.json](2025/NBT24-total-feed-in-rates.json)

- **[archives/](https://github.com/danielraffel/pge-feed-in-rates/tree/main/archives)**: Contains comprehensive JSON files with complete feed-in rates across all applicable years
  - Example: [archives/NBT24-generation-feed-in-rates.json](archives/NBT24-generation-feed-in-rates.json)
  - Example: [archives/NBT24-delivery-feed-in-rates.json](archives/NBT24-delivery-feed-in-rates.json)
  - Example: [archives/NBT24-total-feed-in-rates.json](archives/NBT24-total-feed-in-rates.json)

- **[utility-rates/](https://github.com/danielraffel/pge-feed-in-rates/tree/main/utililty-rates)**: Contains the original PG&E rate files and conversion script
  - Original PG&E rate files for [NBT23](https://github.com/danielraffel/pge-feed-in-rates/blob/main/utililty-rates/PG%26E%20NBT%20EEC%20Values%202023%20Vintage.csv.zip), [NBT24](https://github.com/danielraffel/pge-feed-in-rates/blob/main/utililty-rates/PG%26E%20NBT%20EEC%20Values%202024%20Vintage.csv.zip), [NBT25](https://github.com/danielraffel/pge-feed-in-rates/blob/main/utililty-rates/PG%26E%20NBT%20EEC%20Values%202025%20Vintage.csv.zip), [NBT26](https://github.com/danielraffel/pge-feed-in-rates/blob/main/utililty-rates/PG%26E%20NBT%20EEC%20Values%202026%20Vintage.csv.zip), and [NBT00](https://github.com/danielraffel/pge-feed-in-rates/blob/main/utililty-rates/PG%26E%20NBT%20EEC%20Values%20Floating%20Vintage.csv.zip) (zipped CSV format)
  - [convert-rates.py](https://github.com/danielraffel/pge-feed-in-rates/blob/main/utililty-rates/convert-rates.py): Python script to convert PG&E rate files to EVCC-compatible JSON
  - [Solar Billing Plan Export Rates Readme.txt](https://github.com/danielraffel/pge-feed-in-rates/blob/main/utililty-rates/Solar%20Billing%20Plan%20Export%20Rates%20Readme.txt): Documentation on PG&E rate files

## Understanding PG&E Feed-in Rates

PG&E's Net Billing Tariff (NBT) provides compensation for solar customers when they export energy back to the grid. Rates are determined by:

- **Vintage Year**: The year you activated your solar system (NBT23, NBT24, etc.)
- **Time of Day**, **Day Type**, and **Month**: Rates vary throughout the day, week, and year
- **Rate Type**: Generation rates, Delivery rates, and Total rates (sum of Generation + Delivery)

### Vintage Years and Rate Guarantees

Per [CPUC Resolution E-5301](https://docs.cpuc.ca.gov/PublishedDocs/Published/G000/M521/K257/521257323.PDF), each NBT vintage has specific guarantees:

- **NBT23, NBT24, NBT25, NBT26**: Guaranteed export rates for 9 years from Permission-To-Operate (PTO) date
- **NBT00 (Floating Vintage)**: Only rates for 2025 and 2026 are actual effective rates.

Any rates beyond the guaranteed period are for illustrative purposes only and not actual effective SBP Export Rates.

### Generation, Delivery, and Total Rates

PG&E provides different types of feed-in rates:

- **Generation Rates** (USCA-XXPG): Compensation for the energy you generate and export
- **Delivery Rates** (USCA-PGXX): Account for the delivery component of exported energy
- **Total Rates**: The sum of Generation and Delivery rates, representing complete compensation for bundled customers

#### Which Rate to Use?

- If you're a **bundled PG&E customer** (meaning you get **both** energy generation and delivery from PG&E), your total export compensation is:
  
  {Total Export Credit} = {Generation Export Rate} + {Delivery Export Rate}
  
  In this case, you should use the **Total Feed-in Rates** files.

- However, if you buy your electricity from a **CCA or Direct Access provider**, PG&E only pays you the **Delivery Export Rate**, and your CCA/DA provider sets its own Generation Export Rate.

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
  { "start": "2025-01-01T00:00:00Z", "end": "2025-01-01T01:00:00Z", "price": 0.05685 },
  { "start": "2025-01-01T01:00:00Z", "end": "2025-01-01T02:00:00Z", "price": 0.05198 }
]
```

EVCC periodically checks these rates (typically once per hour) to determine the current electricity price for your feed-in calculations, allowing for accurate time-of-use pricing.

## Using with EVCC

These JSON files are formatted for [EVCC's tariff system](https://docs.evcc.io/en/docs/tariffs) for use with the [EVCC Custom Plugin](https://docs.evcc.io/en/docs/tariffs#dynamic-electricity-price). You can link to the appropriate GitHub raw file and add it to your `evcc.yaml` configuration as follows:

For bundled PG&E customers (using Total rates):
```yaml
tariffs:
  currency: USD
  feedin:
    type: custom
    forecast:
      source: http
      uri: https://raw.githubusercontent.com/danielraffel/pge-feed-in-rates/refs/heads/main/2025/NBT24-total-feed-in-rates.json
```

Select the JSON file that corresponds to your solar activation year and rate type. For example, if your solar system was activated in 2024, use the NBT24 files. Adjust the year as needed—this file, for instance, retrieves 2025 rates.

## Converting Your Own Rates

To convert rates for future vintage years or to re-run the conversion:

1. Navigate to the `utility-rates` directory
2. Run the script: `python convert-rates.py`

The script can process both zipped and unzipped CSV files (prioritizing zipped if both exist), and will automatically:
- Generate files for each vintage according to its appropriate year range
- Create separate generation, delivery, and total rate JSON files
- Organize files by year and store comprehensive archives

The script handles different NBT vintages with appropriate date ranges:
- **NBT00 (Floating Vintage)**: 2025-2026 only
- **NBT23**: 2023-2031 (9 years) *
- **NBT24**: 2024-2032 (9 years) *
- **NBT25**: 2025-2033 (9 years)
- **NBT26**: 2026-2034 (9 years)
- Future vintages can be easily added and mapped to appropriate 9-year periods

* Note: NBT23 and NBT24 only generate files from 2024 onward

## About the Source Data

- **NBT23, NBT24, NBT25, NBT26**: From `PG&E NBT EEC Values [Year] Vintage.csv.zip` files
- **NBT00**: From `PG&E NBT EEC Values Floating Vintage.csv.zip`

The original source of the PG&E data is available [here](https://www.pge.com/assets/pge/docs/vanities/PGE-Solar-Billing-Plan-Export-Rates.zip).

## Potential Future Features

- Support for creating a new Total Feed-in Rate file based on customers of PG&E who use Delivery Export Rate, and whose CCA/DA provider sets its own Generation Export Rate.

## Not Supported

- Net Surplus Compensation Rates are not currently supported. For more information, refer to [PG&E's Net Surplus Compensation page](https://www.pge.com/en/clean-energy/solar/solar-incentives-and-programs/net-surplus-compensation.html) and their [monthly updated compensation rate PDF](https://www.pge.com/assets/pge/docs/clean-energy/solar/AB920-RateTable.pdf).

## Disclaimer - Use at Your Own Risk

Use this information at your own risk. While every effort has been made to ensure accuracy, this repository is not officially affiliated with PG&E. Always verify rate information with PG&E directly for critical financial decisions.
