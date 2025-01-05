import pandas as pd

# Load the CSV file
input_file = "2_rates_master_us_treasury.csv"
data = pd.read_csv(input_file)

# Convert 'date' column to datetime
data['date'] = pd.to_datetime(data['date'])

# Define the target dates (month and day)
target_dates = ['3/31', '6/30', '9/30', '12/31', '1/31', '4/30', '7/31', '10/31']

# Extract all unique years from the data
years = data['date'].dt.year.unique()

# Generate target dates for each year
full_target_dates = [pd.Timestamp(f"{year}-{target}") for year in years for target in target_dates]
target_df = pd.DataFrame({'date': full_target_dates})

# Sort both data and target_df by date
data = data.sort_values('date')
target_df = target_df.sort_values('date')

# Merge with target dates, keeping only rows from the data closest to target dates
result = pd.merge_asof(
    target_df,
    data,
    on='date',
    direction='backward'
)

# Save the result to a new CSV file
result.to_csv("1_rates_master_us_treasury.csv", index=False)
