# import pandas as pd
# import requests
# import datetime as dt
# from headers import headers

# def myhistory(headers, exchange, symbol_token, interval, start_date, end_date):
#     url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/historical/v1/getCandleData"
    
#     payload = {
#         "exchange": exchange,
#         "symboltoken": symbol_token,
#         "interval": interval,
#         "fromdate": start_date,
#         "todate": end_date
#     }

#     try:
#         response = requests.post(url, json=payload, headers=headers)
#         response.raise_for_status()

#         data = response.json().get('data', [])

#         if data:
#             formatted_data = pd.DataFrame(data, columns=[
#                 "Timestamp", "Open", "High", "Low", "Close", "Volume"
#             ])
#             formatted_data["Timestamp"] = pd.to_datetime(formatted_data["Timestamp"]).dt.tz_localize(None)
#             formatted_data["Open"] = formatted_data["Open"].astype(float)
#             formatted_data["High"] = formatted_data["High"].astype(float)
#             formatted_data["Low"] = formatted_data["Low"].astype(float)
#             formatted_data["Close"] = formatted_data["Close"].astype(float)
#             formatted_data["Volume"] = formatted_data["Volume"].astype(float)

#             return formatted_data
#         else:
#             print("No data returned from API")
#             return pd.DataFrame()

#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching Angel Broking data: {e}")
#         return pd.DataFrame()

# # Read the CSV file into a DataFrame
# csv_file_path = "investment.csv"
# df = pd.read_csv(csv_file_path, header=None)

# # Ensure correct column names
# column_names = ['action', 'quantity', 'stock', 'stock_token', 'date', 'buy_price', 'sl']
# df.columns = column_names

# # Convert end_date_str to datetime
# end_date_str = '2024-06-08 05:30'
# try:
#     end_date = dt.datetime.strptime(end_date_str, '%Y-%m-%d %H:%M')
# except ValueError as e:
#     print(f"Error parsing end_date: {e}")
#     end_date = None

# if end_date is not None:
#     # Calculate start_date as 30 days before the end_date
#     start_date = end_date - dt.timedelta(days=30)

#     # Format dates as strings
#     end_date_str = end_date.strftime('%Y-%m-%d %H:%M')
#     start_date_str = start_date.strftime('%Y-%m-%d %H:%M')

#     print("Start Date:", start_date_str)
#     print("End Date:", end_date_str)

#     # Define variables to store updated data
#     updated_rows = []
#     rows_to_delete = []

#     # Check if DataFrame is empty
#     if df.empty:
#         print("No data to process.")
#     else:
#         # Iterate over each row in the DataFrame
#         for index, row in df.iterrows():
#             stock = row['stock']
#             stock_token = row['stock_token']
#             historical_data = myhistory(headers, "NSE", stock_token, "ONE_DAY", start_date_str, end_date_str)

#             if historical_data.empty:
#                 print(f"No historical data for {stock} with token {stock_token}")
#                 continue

#             if historical_data.shape[0] > 0:
#                 today = historical_data.iloc[-1].copy()  # Create a copy of the row
#                 today["Timestamp"] = today["Timestamp"].tz_localize(None)

#                 # Convert row["date"] to a datetime object
#                 purchase_date = dt.datetime.strptime(row["date"], '%Y-%m-%d')

#                 # Generate business date range
#                 bdate_range = pd.bdate_range(start=purchase_date, periods=24)  # Get the next 24 business days
#                 print(bdate_range)

#                 if len(bdate_range) == 24:
#                     max_holding_date = bdate_range[-1]
#                     print(f"Max holding date for {stock}: {max_holding_date}")

#                     # Check if today is before the max holding date
#                     if today["Timestamp"].date() < max_holding_date.date():
#                         print(f"Within holding period for {stock}.")
#                     else:
#                         print(f"Exceeded holding period for {stock}.")

#             else:
#                 print(f"No data available for {stock} with token {stock_token}")

# else:
#     print("Invalid end_date provided. Processing aborted.")


import pandas as pd 

purchase_date = "2021-11-17"

bdate_range = pd.bdate_range(start=purchase_date, periods=24)  # Get the next 24 business days
print(bdate_range)