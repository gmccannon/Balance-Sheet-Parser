import pandas as pd

# Load the CSV file
input_file = "2_rank_score.csv"
data = pd.read_csv(input_file)

# Convert 'date' column to datetime
data['date'] = pd.to_datetime(data['date'])

# Define the target dates (month and day)
target_dates = ['3/31', '6/30', '9/30', '12/31', '1/31', '4/30', '7/31', '10/31']

# Extract all unique years from the data
years = data['date'].dt.year.unique()

# Initialize the result DataFrame
result = pd.DataFrame()

# Process each symbol separately
for symbol, group in data.groupby('act_symbol'):
    # Generate target dates for each year, specific to this symbol
    full_target_dates = [pd.Timestamp(f"{year}-{target}") for year in years for target in target_dates]
    target_df = pd.DataFrame({'date': full_target_dates, 'act_symbol': symbol})
    
    # Sort both group and target_df by date
    group = group.sort_values('date')
    target_df = target_df.sort_values('date')
    
    # Merge with target dates, keeping only rows from the group closest to target dates
    merged = pd.merge_asof(
        target_df,
        group,
        on='date',
        by='act_symbol',
        direction='backward'
    )
    result = pd.concat([result, merged])

    print(f"Processed symbol: {symbol}")

# Save the result to a new CSV file
result.to_csv("1.2_rank_score.csv", index=False)
