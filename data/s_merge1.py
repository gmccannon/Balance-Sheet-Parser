import pandas as pd

# List of file paths
file_paths = ["1_balance_sheet_assets.csv", "1_balance_sheet_equity.csv", \
              "1_balance_sheet_liabilities.csv", "1_cash_flow_statement.csv", \
              "1_eps_current.csv", "1_eps_next.csv", "1_income_statement.csv", \
                 "1_sales_current.csv", "1_sales_next.csv"]

# Read the CSV files into DataFrames
dataframes = [pd.read_csv(file_path) for file_path in file_paths]

# Join the DataFrames on the columns: date, act_symbol, period
merged_df = dataframes[0]
for df in dataframes[1:]:
    merged_df = pd.merge(merged_df, df, on=["date", "act_symbol", "period"], how="left")

# Save the merged DataFrame to a new CSV
merged_df.to_csv("merged_output.csv", index=False)

print("CSV files successfully merged!")
