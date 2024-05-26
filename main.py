import pandas as pd
import yfinance as yf
import csv

companies = ['TMCI', 'CYBCF', 'CLLXF']

# Initialize a dictionary to hold company metrics
company_metrics = {}

# Loop through each company and fetch financial data
for company in companies:
    company_metrics[company] = {}
    
    company_info = yf.Ticker(company)
    
    # Fetch financial statements
    balance_sheet = company_info.balance_sheet
    cash_flow = company_info.cashflow
    income_statement = company_info.financials
    
    # Store the data in the dictionary
    company_metrics[company]['balance_sheet'] = balance_sheet
    company_metrics[company]['cash_flow'] = cash_flow
    company_metrics[company]['income_statement'] = income_statement

# save all to one sheet
for company in companies:
    with open(f"{company}_combined_financials.csv", 'w') as writer:
        first = True
        for statement_name, statement_data in company_metrics[company].items():
            if isinstance(statement_data, pd.DataFrame):
                df = pd.DataFrame(statement_data)
                df.to_csv(writer, header=first, index=True)
                first = False  # Only include the header in the first write

#transpose
for company in companies:
        combined_df = pd.read_csv(f"{company}_combined_financials.csv", index_col=0)
        transposed_df = combined_df.T
        transposed_df.to_csv(f"{company}_combined_financials.csv", header=True, index=True)

# Name the first column 'Date'
for company in companies:
    # Open the CSV file for reading
    with open(f"{company}_combined_financials.csv", newline='') as csvfile:
        lines = csvfile.readlines()
    # Add 'Date' before the first comma in the header row
    lines[0] = 'Date' + lines[0]
    # Write the modified content back to the CSV file
    with open(f"{company}_combined_financials.csv", 'w', newline='') as csvfile:
        csvfile.writelines(lines)

# calc price, remove the whole row if no price can be found
for company in companies:
    with open(f"{company}_combined_financials.csv", newline='') as csvfile:
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
        df.to_csv(f"{company}_combined_financials.csv", index=False)

# calc price change in 1 year (target variable for ML)
for company in companies:
    with open(f"{company}_combined_financials.csv", newline='') as csvfile:
        # Read the CSV file
        df = pd.read_csv(csvfile)
        df['Price Change'] = float('nan')
        for i, date in df.iloc[:, 0].items():      
            try: 
                df.at[i, 'Price Change'] = df.at[i - 1, 'Price']/df.at[i, 'Price']
            except:
                pass
        # Write
        df.to_csv(f"{company}_combined_financials.csv", index=False)
