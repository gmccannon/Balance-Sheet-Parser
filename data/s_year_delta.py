import pandas as pd

# Load the CSV file
df = pd.read_csv('year_data.csv')

# Drop 4 date columns
df = df.drop(columns=['hv_year_high_date', 'hv_year_low_date', 'iv_year_high_date', 'iv_year_low_date'])

# Change Buy, Hold, Sell in rank columns to numerical values
df['rank'] = df['rank'].map({'Buy': 1, 'Hold': 2, 'Sell': 3})

# Change grades in value, growth, momentum, vgm to numerical values
df['value'] = df['value'].map({'A': 1, 'B': 2, 'C': 3, 'D': 4, 'F': 5})
df['growth'] = df['growth'].map({'A': 1, 'B': 2, 'C': 3, 'D': 4, 'F': 5})
df['momentum'] = df['momentum'].map({'A': 1, 'B': 2, 'C': 3, 'D': 4, 'F': 5})
df['vgm'] = df['vgm'].map({'A': 1, 'B': 2, 'C': 3, 'D': 4, 'F': 5})

# Sort the dataframe by 'act_symbol' and 'date' to ensure proper order
df.sort_values(by=['act_symbol', 'date'], inplace=True)

# Function to calculate the ratio for non-price columns (current_value / previous_value)
def calc_ratios(group, non_price_columns):
    # Calculate ratios for non-price columns: current_value / previous_value
    group[non_price_columns] = group[non_price_columns].div(group[non_price_columns].shift(1))
    
    # Handle zero division and NaN by replacing with 0
    group[non_price_columns].replace([float('inf'), -float('inf')], 0, inplace=True)
    group[non_price_columns].fillna(0, inplace=True)
    
    # Calculate the price ratio (next_value / current_value) for adjusted_price
    group['adjusted_price'] = group['adjusted_price'].shift(-1) / group['adjusted_price']
    group['adjusted_price'].iloc[-1] = None  # Set last row to null as there's no next row

    # Handle zero division and NaN for price ratio
    group['adjusted_price'].replace([float('inf'), -float('inf')], 0, inplace=True)
    group['adjusted_price'].fillna(0, inplace=True)

    return group

# Get the list of non-price columns (columns from 4th to last)
non_price_columns = df.columns[3:]

# Process each group of 'act_symbol'
df = df.groupby('act_symbol', group_keys=False).apply(lambda group: calc_ratios(group, non_price_columns))

# Drop the first row in each group (no previous value for non-price columns)
df = df.groupby('act_symbol').apply(lambda group: group.iloc[1:]).reset_index(drop=True)

# Save the modified dataframe to a new CSV
df.to_csv('year_delta.csv', index=False)
