import pandas as pd

# List of file paths
file_paths = ["merged_output.csv", "1.2_options_master_volatility_history.csv", "1.2_prices.csv", "1.2_rank_score.csv", "1.2_eps_history.csv"]

# Read the CSV files into DataFrames
dataframes = [pd.read_csv(file_path) for file_path in file_paths]

# Join the DataFrames on the columns: date, act_symbol, period
merged_df = dataframes[0]
for df in dataframes[1:]:
    merged_df = pd.merge(merged_df, df, on=["date", "act_symbol"], how="left")

# Save the merged DataFrame to a new CSV
merged_df.to_csv("merged_output2.csv", index=False)

print("CSV files successfully merged!")
