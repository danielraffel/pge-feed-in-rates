# PG&E Feed-in Rates

This repository provides PG&E feed-in rate data in JSON format for use with energy management systems like [EVCC](https://evcc.io). The data is particularly useful for PG&E solar customers who want to track their energy usage based on the rates they receive when exporting energy back to the grid.

## Repository Structure

- **`2025/`**: This folder contains JSON files with feed-in rates specifically for the 2025 calendar year. Each file is structured to match EVCC's expected format, ensuring seamless integration with the [EVCC Custom Plugin](https://docs.evcc.io/en/docs/tariffs#custom-plugin).
  - `NBT23-generation-feed-in-rates.json`: Generation rates for customers who activated solar in 2023
  - `NBT23-delivery-feed-in-rates.json`: Delivery rates for customers who activated solar in 2023
  - `NBT24-generation-feed-in-rates.json`: Generation rates for customers who activated solar in 2024
  - `NBT24-delivery-feed-in-rates.json`: Delivery rates for customers who activated solar in 2024
  - `NBT25-generation-feed-in-rates.json`: Generation rates for customers who activated solar in 2025
  - `NBT25-delivery-feed-in-rates.json`: Delivery rates for customers who activated solar in 2025

- **`scripts/`**: Contains utilities for converting PG&E CSV rate files to JSON
  - `convert_rates.py`: Python script to convert PG&E CSV rate files to EVCC-compatible JSON format

- **`utility-rates/`**: Contains the original PG&E rate files
  - `Solar Billing Plan Export Rates Readme.txt`: PG&E's documentation explaining their rate files
  - `PG&E NBT EEC Values 2023 Vintage.csv.zip`: Solar Billing Plan Customers with applications filed in 2023 that qualify for 9-year lock-in export rates
  - `PG&E NBT EEC Values 2024 Vintage.csv.zip`: Solar Billing Plan Customers with applications filed in 2024 that qualify for 9-year lock-in export rates
  - `PG&E NBT EEC Values 2025 Vintage.csv.zip`: Solar Billing Plan Customers with applications filed in 2025 that qualify for 9-year lock-in export rates
  - `PG&E NBT EEC Values 2026 Vintage.csv.zip`: Solar Billing Plan Customers with applications filed in 2026 that qualify for 9-year lock-in export rates

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
   * `/2025/NBT23-delivery-feed-in-rates.json`: 2025 delivery rates for Solar Billing Plan Customers with applications filed in 2023
   * `/2025/NBT23-generation-feed-in-rates.json`: 2025 generation rates for Solar Billing Plan Customers with applications filed in 2023
   * `/2025/NBT24-delivery-feed-in-rates.json`: 2025 delivery rates for Solar Billing Plan Customers with applications filed in 2024
   * `/2025/NBT24-generation-feed-in-rates.json`: 2025 generation rates for Solar Billing Plan Customers with applications filed in 2024
   * `/2025/NBT25-delivery-feed-in-rates.json`: 2025 delivery rates for Solar Billing Plan Customers with applications filed in 2025
   * `/2025/NBT25-generation-feed-in-rates.json`: 2025 generation rates for Solar Billing Plan Customers with applications filed in 2025

EVCC will pull this data hourly to optimize your energy usage based on the current feed-in rates.

## Converting Your Own Rates

If you need to convert rates for a different vintage year or future calendar years, you can use the provided Python script:

1. Place your PG&E CSV file in the same directory as the Python script. The script assumes the file is named something like `PG&E NBT EEC Values 2024 Vintage.csv`.
2. Run the script:
   ```
   python convert_rates.py
   ```
3. The script will automatically process all PG&E NBT EEC Values CSV files in the directory, creating both generation and delivery rate JSON files organized by year

The script will create separate JSON files for generation and delivery rates, with appropriate naming to reflect the vintage year and rate type.

## About the Rate Files

PG&E is required to provide 20-years of export rates. However please note that NBT23, NBT24, NBT25, and NBT26 vintage customers are only guaranteed export rates for 9-years from the Permission-To-Operate (PTO) date of your system. Any rate factors in this file beyond the 9-year lock-in period are for illustrative purposes only and are not actual effective SBP Export Rates at those times. 

Feel free to use these files in your own energy management system. The data is pulled directly from [PG&E's official rate files](https://www.pge.com/assets/pge/docs/vanities/PGE-Solar-Billing-Plan-Export-Rates.zip), which are legally required to be publicly available.

## Appendix

As if this wasn't already confusing enough, the original PG&E README text appears to have errors in its description of the PG&E NBT EEC Vintage files. I've corrected these in my version hosted here.

## Disclaimer

While every effort has been made to ensure accuracy, this repository is not officially affiliated with PG&E. Always verify rate information with PG&E for critical financial decisions.
