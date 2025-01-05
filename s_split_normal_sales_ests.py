from datetime import timedelta
import pandas as pd

# Load the CSV file
input_file = "2_sales_estimate.csv"
data = pd.read_csv(input_file)

# Drop the period_end_date column
data = data.drop(columns=['period_end_date'])

# Convert 'date' column to datetime
data['date'] = pd.to_datetime(data['date'])

# Define the reference dates (month and day only)
reference_dates = ['3/31', '6/30', '9/30', '12/31', '1/31', '4/30', '7/31', '10/31']

# Get all unique years in the data
years = data['date'].dt.year.unique()

# Generate reference dates for all years
full_reference_dates = []
for year in years:
    for ref_date in reference_dates:
        full_reference_dates.append(pd.Timestamp(f"{year}/{ref_date}"))

# Create ranges (one week before and including each reference date)
ranges = [(date - timedelta(days=7), date) for date in full_reference_dates]

# Filter rows within any of the date ranges
mask = data['date'].apply(lambda x: any(start <= x <= end for start, end in ranges))
sorted_data = data[mask]

# Adjust the dates to be the last day of the month
sorted_data['date'] = sorted_data['date'] + pd.offsets.MonthEnd(0)

# Split the data based on the 'period' column
current_periods = sorted_data[sorted_data['period'].isin(['Current Quarter', 'Current Year'])]
next_periods = sorted_data[sorted_data['period'].isin(['Next Quarter', 'Next Year'])]

# Remove 'Current' and 'Next' from the 'period' column
current_periods['period'] = current_periods['period'].str.replace('Current ', '', regex=False)
next_periods['period'] = next_periods['period'].str.replace('Next ', '', regex=False)

# Prefix the column names in current with sales_current_
current_periods = current_periods.rename(columns={
    'consensus': 'sales_current_consensus',
    'recent': 'sales_current_recent',
    'count': 'sales_current_count',
    'high': 'sales_current_high',
    'low': 'sales_current_low',
    'year_ago': 'sales_current_year_ago'
})

# Prefix the column names in current with sales_current_
next_periods = next_periods.rename(columns={
    'consensus': 'sales_next_consensus',
    'recent': 'sales_next_recent',
    'count': 'sales_next_count',
    'high': 'sales_next_high',
    'low': 'sales_next_low',
    'year_ago': 'sales_next_year_ago'
})

# Remove duplicates
current_periods = current_periods.drop_duplicates()
next_periods = next_periods.drop_duplicates()

# Save the results to separate CSV files
current_periods.to_csv("1_sales_current.csv", index=False)
next_periods.to_csv("1_sales_next.csv", index=False)
