import pandas as pd

# Load the CSV file
input_file = "merged_sorted_output3.csv"
data = pd.read_csv(input_file)

# Get the rows where period is year, then drop the 'period' column, drops rows with no adjusted_price
year_data = data[data['period'] == 'Year']
year_data = year_data.drop(columns=['period'])
year_data = year_data.dropna(subset=['adjusted_price'])

# Get the rows where period is quarter, then drop the 'period' column, drops rows with no adjusted_price
quarter_data = data[data['period'] == 'Quarter']
quarter_data = quarter_data.drop(columns=['period'])
quarter_data = quarter_data.dropna(subset=['adjusted_price'])

# Write the dataframes to new CSV files
year_data.to_csv("year_data.csv", index=False)
quarter_data.to_csv("quarter_data.csv", index=False)
