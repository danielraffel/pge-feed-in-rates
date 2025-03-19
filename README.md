# PG&E Feed-in Rates

This repository provides PG&E feed-in rate data in JSON format for use with energy management systems like [EVCC](https://evcc.io). The data is particularly useful for PG&E solar customers who want to optimize their energy usage based on the rates they receive when exporting energy back to the grid.

## Repository Structure

- **`2025/`**: This folder contains JSON files with feed-in rates specifically for the 2025 calendar year. Each file is structured to match EVCC’s expected format, ensuring seamless integration with the [EVCC Custom Plugin](https://docs.evcc.io/en/docs/tariffs#custom-plugin).
  - `NBT24-feed-in-rates.json`: For customers who activated solar in 2024
  - `NBT25-feed-in-rates.json`: For customers who activated solar in 2025

- **`scripts/`**: Contains utilities for converting PG&E CSV rate files to JSON
  - `convert_rates.py`: Python script to convert PG&E CSV rate files to EVCC-compatible JSON format

- **`utility-rates/`**: Contains the original and processed PG&E rate files
  - `Solar Billing Plan Export Rates Readme.txt`: PG&E's documentation explaining their rate files
  - `PG&E NBT EEC Values 2024 Vintage.csv.zip`: Solar Billing Plan Customers with applications filed in 2024 that qualify for 9-year lock-in export rates
  - `PG&E NBT EEC Values 2025 Vintage.csv.zip`: Solar Billing Plan Customers with applications filed in 2025 that qualify for 9-year lock-in export rates
  - `NBT24-2025-only.csv`: Extracted 2025 rates for Solar Billing Plan Customers with applications filed in 2024
  - `NBT25-2025-only.csv`: Extracted 2025 rates for Solar Billing Plan Customers with applications filed in 2025
  - `NBT25-2026-only.csv`: Extracted 2026 rates for Solar Billing Plan Customers with applications filed in 2025
  - `NBT25-2027-only.csv`: Extracted 2027 rates for Solar Billing Plan Customers with applications filed in 2025

## Understanding PG&E Feed-in Rates

PG&E's Net Billing Tariff (NBT) provides compensation for solar customers when they export energy back to the grid. The rates vary by:

- **Vintage Year**: The year you activated your solar system determines your "vintage" rate structure
- **Time of Day**: Export rates vary throughout the day based on demand
- **Day Type**: Different rates for weekdays vs. weekends/holidays
- **Month**: Seasonal variations in rates

The "NBT" number (NBT24, NBT25, etc.) represents the vintage year of the rate plan. For example, if you activated your solar system in 2024, you would use the NBT24 rates.

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
      uri: https://raw.githubusercontent.com/danielraffel/pge-feed-in-rates/refs/heads/main/2025/NBT24-feed-in-rates.json
```

2. Choose the correct JSON file based on your solar activation year:
   - `/2025/NBT24-feed-in-rates.json` 2025 rates for Solar Billing Plan Customers with applications filed in 2024
   - `/2025/NBT25-feed-in-rates.json` 2025 rates for Solar Billing Plan Customers with applications filed in 2025
   - `/2026/NBT25-feed-in-rates.json` 2026 rates for Solar Billing Plan Customers with applications filed in 2025
   - `/2027/NBT25-feed-in-rates.json` 2027 rates for Solar Billing Plan Customers with applications filed in 2025

EVCC will pull this data hourly to optimize your energy usage based on the current feed-in rates.

## Converting Your Own Rates

If you need to convert rates for a different vintage year or future calendar years, you can use the provided Python script:

1. Place your PG&E CSV file in the same directory as the python script
2. Rename the CSV file to `2025.csv` (or modify the script to use your filename)
3. Run the script:
   ```
   python convert_rates.py
   ```
4. The script will generate a `feed-in-rates.json` file in the same directory

## About the Rate Files

PG&E is required to provide 20-years of export rates. However please note that NBT23, NBT24, NBT25, and NBT26 vintage customers are only guaranteed export rates for 9-years from the Permission-To-Operate (PTO) date of your system. Any rate factors in this file beyond the  9-year lock-in period are for illustrative purposes only and are not actual effective SBP Export Rates at those times. 

Feel free to use these files in your own energy management system. The data is pulled directly from PG&E's official rate files, which are legally required to be publicly available.

## Note on this Repositoy

I didn’t initially think to generalize my script for generating a 9-year rate plan for all PG&E NBT EEC values. I sorta figured out how this data was organized on the fly while writing a quick script and, to be honest, I’m not too motivated to generate 9-year rate plans—even for myself—since PG&E will likely push me into a new plan that changes my rates anyway! It’s absurd how unnecessarily complicated this all is. So frustrating!

## Appendix

If you are interested in the original source of the PG&E data you can find it [here](https://www.pge.com/assets/pge/docs/vanities/PGE-Solar-Billing-Plan-Export-Rates.zip). As if this wasn’t already confusing enough, the original PG&E README text appears to have errors in its description of the PG&E NBT EEC Vintage files. I’ve corrected these in my version hosted here.

## Disclaimer

While every effort has been made to ensure accuracy, this repository is not officially affiliated with PG&E. Always verify rate information with PG&E for critical financial decisions.
