import pandas as pd
import yfinance as yf
import csv
import os

companies = []
with open('./tickers/alltickers.txt') as tickers:
    for line in tickers:
        companies.append(line.strip())

# Initialize a dictionary to hold company metrics
company_metrics = {}

# Loop through each company and fetch financial data
for company in companies:
    company_metrics[company] = {}
    
    company_info = yf.Ticker(company)
    
    # Fetch financial statements
    balance_sheet = company_info.quarterly_balance_sheet   
    cash_flow = company_info.quarterly_cashflow
    income_statement = company_info.quarterly_financials
    
    # Store the data in the dictionary
    company_metrics[company]['balance_sheet'] = balance_sheet
    company_metrics[company]['cash_flow'] = cash_flow
    company_metrics[company]['income_statement'] = income_statement

    print(f'Getting sheets: {company}')

# save all to one sheet
for company in companies:
    with open(f"./temps/{company}_combined_financials_not_t.csv", 'w') as writer:
        first = True
        for statement_name, statement_data in company_metrics[company].items():
            if isinstance(statement_data, pd.DataFrame):
                df = pd.DataFrame(statement_data)
                df.to_csv(writer, header=first, index=True)
                first = False  # Only include the header in the first write

# fix the length of the downloaded files
for company in companies:
    with open(f"./temps/{company}_combined_financials_not_t.csv", 'r') as input_csv, \
         open(f"./temps/{company}_combined_financials.csv", 'w', newline='') as output_csv:
        reader = csv.reader(input_csv)
        writer = csv.writer(output_csv)

        # Get maximum number of columns from the header
        header = next(reader)
        max_columns = len(header)

        # Write header to the output file
        writer.writerow(header)

        # Process each row and remove excess columns
        for row in reader:
            if len(row) > max_columns:
                row = row[:max_columns]  # Remove excess columns
            writer.writerow(row)

#transpose
for company in companies:
    combined_df = pd.read_csv(f"./temps/{company}_combined_financials.csv", index_col=0)
    transposed_df = combined_df.T
    transposed_df.to_csv(f"./temps/{company}_combined_financials.csv", header=True, index=True)

# Name the first column 'Date'
for company in companies:
    # Open the CSV file for reading
    with open(f"./temps/{company}_combined_financials.csv", newline='') as csvfile:
        lines = csvfile.readlines()
    # Add 'Date' before the first comma in the header row
    lines[0] = 'Date' + lines[0]
    # Write the modified content back to the CSV file
    with open(f"./temps/{company}_combined_financials.csv", 'w', newline='') as csvfile:
        csvfile.writelines(lines)

# calc price, remove the whole row if no price can be found
for company in companies:
    with open(f"./temps/{company}_combined_financials.csv", newline='') as csvfile:
        # Read the CSV file
        df = pd.read_csv(csvfile)
        df['Price'] = float('nan')
        for i, date in df.iloc[:, 0].items():
            date_found = False
            start_date = pd.to_datetime(date) - pd.Timedelta(days=10)
            end_date = pd.to_datetime(date) + pd.Timedelta(days=10)
            try:
                # Download stock data for the specified range
                stock_data = yf.download(company, start=start_date, end=end_date)
                # Iterate over the range from 20 days prior to 20 days after
                for single_date in pd.date_range(start=start_date, end=end_date):
                    if single_date in stock_data.index:
                        closing_price = stock_data.loc[single_date, 'Close']
                        df.at[i, 'Price'] = closing_price
                        date_found = True
                        break   
            except Exception as e:
                print(f"Error fetching price for {company} on {date}: {e}")
        # Drop rows where the price could not be obtained
        df = df.dropna(subset=['Price'])

        # Write
        df.to_csv(f"./temps/{company}_combined_financials.csv", index=False)
    
    print(f'Getting price: {company}')

# calc price change in 1 year (target variable for ML)
for company in companies:
    with open(f"./temps/{company}_combined_financials.csv", newline='') as csvfile:
        # Read the CSV file
        df = pd.read_csv(csvfile)
        df['Price Change'] = float('nan')
        for i, date in df.iloc[:, 0].items():      
            try: 
                df.at[i, 'Price Change'] = df.at[i - 1, 'Price']/df.at[i, 'Price']
            except:
                pass
        # Write
        df.to_csv(f"./temps/{company}_combined_financials.csv", index=False)

# Combine all CSVs
unique_headers = set()
for company in companies:
    with open(f"./temps/{company}_combined_financials.csv", newline='') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        if headers:
            unique_headers.update(headers)
# Sort the headers alphabetically for consistency
sorted_headers = sorted(unique_headers)
# Arange the stuff I care about
if 'Date' in sorted_headers:
    sorted_headers.remove('Date')
    sorted_headers.insert(0, 'Date')
if 'Price' in sorted_headers:
    sorted_headers.remove('Price')
    sorted_headers.insert(1, 'Price')
if 'Price Change' in sorted_headers:
    sorted_headers.remove('Price Change')
    sorted_headers.insert(2, 'Price Change')
# Write combined data to a new CSV file
with open('./temps/combined.csv', 'w', newline='') as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=sorted_headers)
    writer.writeheader()
    for company in companies:
        with open(f"./temps/{company}_combined_financials.csv", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Rename variables in the 'Date' column
                if 'Date' in row:
                    row['Date'] = company + '_' + row['Date']
                for header in sorted_headers:
                    # Fill missing values with "NA"
                    if header not in row:
                        row[header] = "NA"
                writer.writerow(row)

# Add NA
with open('./temps/combined.csv', 'r') as input_csv, \
         open('./temps/noNAcombined.csv', 'w', newline='') as output_csv:
        
        reader = csv.reader(input_csv)
        writer = csv.writer(output_csv)

        for row in reader:
            # Replace empty values with 'NA'
            modified_row = ['NA' if cell.strip() == '' else cell for cell in row]
            writer.writerow(modified_row)

# seperate into files to train with, and current dates to make a predicition on
with open('./temps/noNAcombined.csv', 'r') as input_csv, \
        open('q_pred.csv', 'w', newline='') as na_csv, \
        open('q_train.csv', 'w', newline='') as not_na_csv:
    
    reader = csv.DictReader(input_csv)
    na_writer = csv.DictWriter(na_csv, fieldnames=reader.fieldnames)
    not_na_writer = csv.DictWriter(not_na_csv, fieldnames=reader.fieldnames)

    na_writer.writeheader()
    not_na_writer.writeheader()

    for row in reader:
        if row['Price Change'] == 'NA':
            na_writer.writerow(row)
        else:
            not_na_writer.writerow(row)
