import pandas as pd

# Load the CSV file
input_file = "merged_output3.csv"
data = pd.read_csv(input_file)

# Reorder columns to have 'act_symbol', 'date', 'period' and 'adjusted_price' first
data = data[['act_symbol', 'date', 'period', 'adjusted_price'] + [col for col in data.columns if col not in ['act_symbol', 'date', 'period', 'adjusted_price']]]

# Convert 'date' column to datetime for proper sorting
data['date'] = pd.to_datetime(data['date'])

# Sort by 'period', 'act_symbol', and 'date'
data = data.sort_values(by=['act_symbol', 'period', 'date'])

# Drop rows with missing 'act_symbol' or 'date'
data = data.dropna(subset=['act_symbol', 'date'])

# Drop duplicates based on 'act_symbol', 'date', and 'period'
data = data.drop_duplicates(subset=['act_symbol', 'date', 'period'])

# Save the sorted and reordered DataFrame back to CSV
data.to_csv("merged_sorted_output3.csv", index=False)
