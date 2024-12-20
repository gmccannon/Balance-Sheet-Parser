import pandas as pd

# File paths
file1 = 'all_train_data.csv'
file2 = 'current_pred.csv'

# Read the CSV files into DataFrames
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Get the columns that are in one file but not the other
columns_in_file1_not_in_file2 = set(df1.columns) - set(df2.columns)
columns_in_file2_not_in_file1 = set(df2.columns) - set(df1.columns)

# Display the results
if not columns_in_file1_not_in_file2 and not columns_in_file2_not_in_file1:
    print("The CSV files have identical columns.")
else:
    if columns_in_file1_not_in_file2:
        print(f"Columns in {file1} but not in {file2}: {columns_in_file1_not_in_file2}")
    if columns_in_file2_not_in_file1:
        print(f"Columns in {file2} but not in {file1}: {columns_in_file2_not_in_file1}")
