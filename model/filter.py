import csv

# Open the CSV file for reading
with open('q_y_output.csv', 'r') as csvfile:
    # Create a CSV reader object
    reader = csv.DictReader(csvfile)
    
    # Iterate through each row in the CSV file
    for row in reader:
        # Extract Ticker_Date and Predicted_Change values from the current row
        ticker_date = row['Ticker_Date']
        Predicted_Change = float(row['Predicted_Change'])  # Convert to float
        
        # Check if Predicted_Change is greater than 50
        if 4 > Predicted_Change > 3:
            # Print the row
            print(f'Ticker_Date: {ticker_date}, Predicted_Change: {Predicted_Change}')
