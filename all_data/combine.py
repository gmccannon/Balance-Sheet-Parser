import pandas as pd

# File paths
file1 = 'dec2024/q_train.csv'
file2 = 'july2024/q_train.csv'
output_file = 'all_train_data.csv'

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Combine the two DataFrames
combined_df = pd.concat([df1, df2], ignore_index=True)

# Remove duplicates based on all columns
unique_df = combined_df.drop_duplicates()

# Replace empty cells with 'NA'
unique_df = unique_df.fillna('NA')

# Sort rows alphabetically by the 'Date' column, ensuring underscores come first
unique_df = unique_df.sort_values(by='Date', ascending=True, key=lambda x: x.str.replace('_', ' ', regex=False))

# Save the resulting DataFrame to a new CSV
unique_df.to_csv(output_file, index=False)

print(f"Combined and sorted CSV saved to {output_file}")
