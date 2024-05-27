import csv

# Open the CSV file for reading
with open('output.csv', 'r') as csvfile:
    # Create a CSV reader object
    reader = csv.DictReader(csvfile)
    
    # Iterate through each row in the CSV file
    for row in reader:
        # Extract Ticker_Date and Price_Predicted values from the current row
        ticker_date = row['Ticker_Date']
        price_predicted = float(row['Price_Predicted'])  # Convert to float
        
        # Check if Price_Predicted is greater than 50
        if 6 > price_predicted > 5:
            # Print the row
            print(f'Ticker_Date: {ticker_date}, Price_Predicted: {price_predicted}')
