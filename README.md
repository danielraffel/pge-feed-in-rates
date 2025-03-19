# PG&E Feed-in Rates

This repository provides PG&E feed-in rate data in JSON format for use with energy management systems like [EVCC](https://evcc.io). The data is particularly useful for PG&E solar customers who want to track their energy usage based on the rates they receive when exporting energy back to the grid.

## Repository Structure

- **`2025/`**: This folder contains JSON files with feed-in rates specifically for the 2025 calendar year. Similar folders exist for each year from 2025 to 2033, ensuring a multi-year dataset. Each file is structured to match EVCC's expected format, ensuring seamless integration with the [EVCC Custom Plugin](https://docs.evcc.io/en/docs/tariffs#custom-plugin).
  - `NBT23-generation-feed-in-rates.json`: Generation rates for customers who activated solar in 2023
  - `NBT23-delivery-feed-in-rates.json`: Delivery rates for customers who activated solar in 2023
  - `NBT24-generation-feed-in-rates.json`: Generation rates for customers who activated solar in 2024
  - `NBT24-delivery-feed-in-rates.json`: Delivery rates for customers who activated solar in 2024
  - `NBT25-generation-feed-in-rates.json`: Generation rates for customers who activated solar in 2025
  - `NBT25-delivery-feed-in-rates.json`: Delivery rates for customers who activated solar in 2025
  - `NBT26-generation-feed-in-rates.json`: Generation rates for customers who activated solar in 2026
  - `NBT26-delivery-feed-in-rates.json`: Delivery rates for customers who activated solar in 2026

- **`2025-2033/`**: This folder contains comprehensive JSON files with feed-in rates spanning from 2025 to 2033. These files combine multiple years of data into a single file for convenience.
  - `NBT23-delivery-feed-in-rates.json`: Complete 9-year delivery rates for 2023 vintage customers
  - `NBT23-generation-feed-in-rates.json`: Complete 9-year generation rates for 2023 vintage customers
  - `NBT24-delivery-feed-in-rates.json`: Complete 9-year delivery rates for 2024 vintage customers
  - `NBT24-generation-feed-in-rates.json`: Complete 9-year generation rates for 2024 vintage customers
  - `NBT25-delivery-feed-in-rates.json`: Complete 9-year delivery rates for 2025 vintage customers
  - `NBT25-generation-feed-in-rates.json`: Complete 9-year generation rates for 2025 vintage customers
  - `NBT26-delivery-feed-in-rates.json`: 8-year delivery rates for 2026 vintage customers
  - `NBT26-generation-feed-in-rates.json`: 8-year generation rates for 2026 vintage customers

- **`scripts/`**: Contains a python script for converting PG&E CSV rate files to JSON
  - `convert_rates.py`: Python script to convert PG&E CSV rate files to EVCC-compatible JSON format

- **`utility-rates/`**: Contains the original PG&E rate files
  - `Solar Billing Plan Export Rates Readme.txt`: PG&E's documentation explaining their rate files
  - `PG&E NBT EEC Values 2023 Vintage.csv.zip`: Solar Billing Plan (SBP) Customers with applications filed in 2023 that qualify for 9-year lock-in export rates
  - `PG&E NBT EEC Values 2024 Vintage.csv.zip`: SBP Customers with applications filed in 2024 that qualify for 9-year lock-in export rates
  - `PG&E NBT EEC Values 2025 Vintage.csv.zip`: SBP Customers with applications filed in 2025 that qualify for 9-year lock-in export rates
  - `PG&E NBT EEC Values 2026 Vintage.csv.zip`: SBP Customers with applications filed in 2026 that qualify for 9-year lock-in export rates

## Understanding PG&E Feed-in Rates

PG&E's Net Billing Tariff (NBT) provides compensation for solar customers when they export energy back to the grid. The rates vary by:

- **Vintage Year**: The year you activated your solar system determines your "vintage" rate structure
- **Time of Day**: Export rates vary throughout the day based on demand
- **Day Type**: Different rates for weekdays vs. weekends/holidays
- **Month**: Seasonal variations in rates
- **Rate Type**: Generation rates vs. Delivery rates

The "NBT" number (NBT23, NBT24, etc.) represents the vintage year of the rate plan. For example, if you activated your solar system in 2024, you would use the NBT24 rates.

### Generation vs. Delivery Rates

PG&E's rate files distinguish between two types of feed-in rates:

- **Generation Rates**: These rates (identified by "USCA-XXPG" in PG&E's rate files) represent compensation for the energy you generate and export to the grid.
- **Delivery Rates**: These rates (identified by "USCA-PGXX" in PG&E's rate files) account for the delivery component of your exported energy.

For most home solar customers, the generation rates are typically the most relevant for calculating export compensation.

Note: Generation Export Rates are only applicable to Solar Billing Plan (SBP) customers that receive bundled generation service from PG&E. Customers that receive generation service from a Community Choice Aggregator (CCA) or a Direct Access (DA) provider should refer to that generation service provider for more information about the generation export pricing available to them.

## Using with EVCC

These JSON files are formatted specifically for use with [EVCC's tariff system](https://docs.evcc.io/en/docs/tariffs). To use them in your EVCC configuration:

1. Add the feed-in section to your `evcc.yaml` file:

```yaml
tariffs:
  currency: USD
  feedin:
    type: custom
    forecast:
      source: http
      uri: https://raw.githubusercontent.com/danielraffel/pge-feed-in-rates/refs/heads/main/2025/NBT24-generation-feed-in-rates.json
```

2. Choose the correct JSON file for your current rate based on your solar activation year and whether you want generation vs delivery rates:
   
   **For specific year rates (2025):**
   * `/2025/NBT23-delivery-feed-in-rates.json`: 2025 delivery rates for SBP Customers with applications filed in 2023
   * `/2025/NBT23-generation-feed-in-rates.json`: 2025 generation rates for SBP Customers with applications filed in 2023
   * `/2025/NBT24-delivery-feed-in-rates.json`: 2025 delivery rates for SBP Customers with applications filed in 2024
   * `/2025/NBT24-generation-feed-in-rates.json`: 2025 generation rates for SBP Customers with applications filed in 2024
   * `/2025/NBT25-delivery-feed-in-rates.json`: 2025 delivery rates for SBP Customers with applications filed in 2025
   * `/2025/NBT25-generation-feed-in-rates.json`: 2025 generation rates for SBP Customers with applications filed in 2025
   * `/2025/NBT26-delivery-feed-in-rates.json`: 2025 delivery rates for SBP Customers with applications filed in 2026
   * `/2025/NBT26-generation-feed-in-rates.json`: 2025 generation rates for SBP Customers with applications filed in 2026
   
   **For comprehensive multi-year rates (2025-2033):**
   * `/2025-2033/NBT23-delivery-feed-in-rates.json`: Complete 9-year delivery rates for 2023 vintage customers
   * `/2025-2033/NBT23-generation-feed-in-rates.json`: Complete 9-year generation rates for 2023 vintage customers
   * `/2025-2033/NBT24-delivery-feed-in-rates.json`: Complete 9-year delivery rates for 2024 vintage customers
   * `/2025-2033/NBT24-generation-feed-in-rates.json`: Complete 9-year generation rates for 2024 vintage customers
   * `/2025-2033/NBT25-delivery-feed-in-rates.json`: Complete 9-year delivery rates for 2025 vintage customers
   * `/2025-2033/NBT25-generation-feed-in-rates.json`: Complete 9-year generation rates for 2025 vintage customers
   * `/2025-2033/NBT26-delivery-feed-in-rates.json`: 8-year delivery rates for 2026 vintage customers
   * `/2025-2033/NBT26-generation-feed-in-rates.json`: 8-year generation rates for 2026 vintage customers

EVCC will pull this data hourly to optimize your energy usage based on the current feed-in rates.

## Converting Your Own Rates

If you need to convert rates for a different vintage year or future calendar years, you can use the provided Python script:

1. Place your PG&E CSV file in the same directory as the python script
2. Run the script:
   ```
   python convert_rates.py
   ```
3. The script will automatically process all PG&E NBT EEC Values CSV files in the directory, creating both generation and delivery rate JSON files organized by year

The script will create separate JSON files for generation and delivery rates, with appropriate naming to reflect the vintage year and rate type. The script that generated this output was written quickly and optimized to produce 9 years of data for customers who activated in 2024. Earlier vintage years will have access to more rate data, while 2026 vintage customers will only have 8 years of rate data available.

## About the Rate Files

PG&E is required to provide 20-years of export rates. However please note that NBT23, NBT24, NBT25, and NBT26 vintage customers are only guaranteed export rates for 9-years from the Permission-To-Operate (PTO) date of your system. Any rate factors in this file beyond the 9-year lock-in period are for illustrative purposes only and are not actual effective SBP Export Rates at those times. 

Feel free to use these files in your own energy management system. The data is pulled directly from PG&E's official rate files, which are legally required to be publicly available.

## Appendix

If you are interested in the original source of the PG&E data you can find it [here](https://www.pge.com/assets/pge/docs/vanities/PGE-Solar-Billing-Plan-Export-Rates.zip). As if this wasn't already confusing enough, the original PG&E README text appears to have errors in its description of the PG&E NBT EEC Vintage files. I've corrected these in my version hosted here.

## Disclaimer

While every effort has been made to ensure accuracy, this repository is not officially affiliated with PG&E. Always verify rate information with PG&E for critical financial decisions.
