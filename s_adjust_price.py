import pandas as pd
import numpy as np

# Read the CSV files
prices_df = pd.read_csv("prices.csv")
splits_df = pd.read_csv("combined_splits.csv")

# Convert date columns to datetime
prices_df['date'] = pd.to_datetime(prices_df['date'])
splits_df['ex_date'] = pd.to_datetime(splits_df['ex_date'])

# Initialize the adjusted price column with the original close price
prices_df['adjusted_price'] = prices_df['close']

# Sort splits by ex_date in ascending order (oldest first)
splits_df = splits_df.sort_values(by='ex_date', ascending=True)

# Iterate over each price row
for idx, price_row in prices_df.iterrows():
    adjustment = 1  # Default adjustment factor

    # Find all splits for this symbol that occurred before the current price date
    relevant_splits = splits_df[(splits_df['act_symbol'] == price_row['act_symbol']) &
                                (splits_df['ex_date'] >= price_row['date'])]

    print(f"Processing {price_row['act_symbol']} on {price_row['date']}")

    # If there are any splits before this price date
    if not relevant_splits.empty:
        print(f"Found {len(relevant_splits)} splits for {price_row['act_symbol']} after {price_row['date']}:")
        
        for _, split_row in relevant_splits.iterrows():
            print(f"Applying split factor {split_row['factor']} from {split_row['ex_date']}")
            adjustment *= split_row['factor']
        
        # Adjust the price
        adjusted_price = price_row['close'] / adjustment
        prices_df.at[idx, 'adjusted_price'] = adjusted_price
        print(f"Adjusted price: {adjusted_price}")
    else:
        print(f"No splits found for {price_row['act_symbol']} before {price_row['date']}")

# Select the relevant columns for the output
output_df = prices_df[['act_symbol', 'date', 'adjusted_price', 'volume']]

# Remove duplicates if any
output_df = output_df.drop_duplicates()

# Sort by symbol and date as requested
output_df = output_df.sort_values(by=['act_symbol', 'date'])

# Save the adjusted prices to a CSV file
output_file = "adjusted_prices.csv"
output_df.to_csv(output_file, index=False)

print(f"Adjusted prices saved to {output_file}")
