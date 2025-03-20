Understanding Export Pricing:

This file contains 20-years of hourly export rates for five sets of PG&E Solar Billing Plan vintages (i.e. Net Billing Tariff / NBT), NBT23,NBT24, NBT25, NBT26, and NBT00. 
-	NBT23 = Solar Billing Plan Customers with applications filed in 2023 that qualify for 9-year lock-in export rates
-	NBT24 = Solar Billing Plan Customers with applications filed in 2024 that qualify for 9-year lock-in export rates
-	NBT25 = Solar Billing Plan Customers with applications filed in 2025 that qualify for 9-year lock-in export rates
-	NBT26 = Solar Billing Plan Customers with applications filed in 2026 that qualify for 9-year lock-in export rates.
-	NBT00 (aka PG&E NBT EEC Values Floating Vintage.csv) = Solar Billing Plan Customers that do not qualify for any 9-year lock-in export rates.
The dates and times associated with the export rates are presented in UTC time, covering from 1/1/2025 12:00:00am PST, to 12/31/2044 11:59:59pm PST.
Per CPUC Resolution E-5301, PG&E is required to provide 20-years of export rates. However please note that NBT23, NBT24, NBT25, and NBT26 vintage customers are only guaranteed export rates for 9-years from the Permission-To-Operate (PTO) date of your system. Any rate factors in this file beyond the  9-year lock-in period are for illustrative purposes only and are not actual effective SBP Export Rates at those times. For NBT00 customers, only those rates for Pacific Standard Time calendar year 2025 and 2026 are actual effective rates, and all rates after that are for illustrative purposes only.

Methodology for calculating the Energy Export Credit Rates from the Most Recently Approved Avoided Cost Calculator:

The Energy Export Credits for a given installation vintage of customers in a given calendar year are based on the applicable vintage of Avoided Cost Calculator (ACC) forecast of values for that year. The following process is used to aggregate values into a single set of values for each month, day-type, and hour for all PG&E customers. This methodology is shared across all Investor Owned Utilities in California.

-	For each Climate Zone, create a set of 8760 hourly avoided costs using the ACC value for the Delivery component, applicable to both bundled and unbundled customers, and the Generation component, applicable only to bundled customers.
-	Take the straight-average ACC value across the Climate Zones for each hour.
-	Adjust time and hour labels to account for daylight savings time because the Avoided Cost Calculator output is in Pacific Standard Time, and identify weekdays and weekend/holidays.
-	For each hourly monthly Delivery and Generation components, calculate the average of all prices by hour, per weekday and weekend. This calculation will render the Energy Export Credit components (Delivery and Generation) for each month’s weekday and weekend values.
-	For each hour and weekday/weekend, the full Energy Export Credit will then be the sum of the corresponding Generation and Delivery components for that hour/weekday/weekend.
Note: Because the Net Billing Tariff (NBT) Energy Export Credits are adjusted for daylight savings time, the date and time labeling has also been adjusted to reflect daylight savings time.

Holidays include New Year’s Day, President’s Day, Memorial Day, Independence Day, Labor Day, Veterans Day, Thanksgiving Day and Christmas Day.

Files Types:

Per CPUC Resolution E-5301, this file contains the export rates in both .csv and .xml formats.


Data Fields Description: 

The following is a description of the data fields in the data file.

RateLookupID Column:

	If the RateLookupID includes “USCA-PGXX” that indicates Delivery Export Rates.

	If the RateLookupID includes “USCA-XXPG” that indicate Generation Export Rates*.

	*Generation Export Rates are only applicable to SBP customers that receive bundled generation service from PG&E. Customers that receive generation service from a Community Choice Aggregator (CCA) or a Direct Access (DA) provider should refer to that generation service provider for more information about the generation export pricing available to them.


RateName Column: 
	The number that follows “NBT” represents the legacy pricing for that year. Please see first paragraph for a description.

Dates and Times Columns:
	DateStart, TimeStart, DateEnd and TimeEnd values are in Coordinated Universal Time (UTC). 

DayStart, DayEnd and ValueName are in Pacific Prevailing Time:
	-	These fields indicate the effective day-type categories of the rate factor
	-	Monday through Sunday are represented as 1-7. Holidays are listed as number “8” in the DayStart and DayEnd columns. 
	-	ValueName Column indicates the month and weekday hour or weekend hour starting value for the rate factor.


Value and Unit Columns:
	This represents the dollar amount pricing per export kWh.
