import pandas as pd

# List of file paths
file_paths = ["merged_output2.csv", "1.5_rates_master_us_treasury.csv"]

# Read the CSV files into DataFrames
dataframes = [pd.read_csv(file_path) for file_path in file_paths]

# Join the DataFrames on the columns: date, act_symbol, period
merged_df = dataframes[0]
for df in dataframes[1:]:
    merged_df = pd.merge(merged_df, df, on=["date"], how="left")

# Save the merged DataFrame to a new CSV
merged_df.to_csv("merged_output3.csv", index=False)

print("CSV files successfully merged!")
