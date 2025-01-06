import pandas as pd

# Input and output file paths
input_file = "splits.csv"  # Replace with your actual file name
output_file = "sorted_splits.csv"

# Read the CSV file
df = pd.read_csv(input_file)

# Create a new DataFrame with the 'act_symbol' and the div of 'to_factor' and 'for_factor'
new_df = pd.DataFrame({
    'act_symbol': df['act_symbol'],
    'ex_date': df['ex_date'],
    'factor': df['to_factor'] / df['for_factor']
})

# Save the sorted DataFrame to a new CSV file
new_df.to_csv(output_file, index=False)

print(f"Sorted and reordered data saved to {output_file}")
