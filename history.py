import requests
import pandas as pd
import csv
import os
import datetime as dt
import time
from headers import headers  # Assuming headers is correctly defined in the headers module

# Function to search for a symbol and token by name in the OpenAPIScripMaster.csv file
def search_symbol_by_name(name, file_path):
    """
    Search for a symbol token and trading symbol by name in a CSV file.

    Parameters:
    - name (str): Name of the symbol to search for.
    - file_path (str): Path to the CSV file containing symbol information.

    Returns:
    - (str, str): Tuple containing symbol token and trading symbol if found, otherwise (None, None).
    """
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['name'] == name and row['symbol'].endswith('-EQ'):
                return row['token'], row['symbol']
    return None, None

# Function to retrieve historical candle data
def myhistory(exchange, symbol_token, interval, start_date, end_date, symbol):
    """
    Fetch historical candle data from Angel Broking API and store in CSV.

    Parameters:
    - exchange (str): Exchange name (e.g., "NSE").
    - symbol_token (str): Symbol token for the company.
    - interval (str): Interval of the candle data (e.g., "ONE_DAY").
    - start_date (str): Start date and time in format '%Y-%m-%d %H:%M'.
    - end_date (str): End date and time in format '%Y-%m-%d %H:%M'.
    - symbol (str): Trading symbol of the company.

    Returns:
    - None
    """
    # Angel Broking API endpoint
    url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/historical/v1/getCandleData"

    # Payload for the request
    payload = {
        "exchange": exchange,
        "symboltoken": symbol_token,
        "interval": interval,
        "fromdate": start_date,
        "todate": end_date
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses

        data = response.json().get('data', [])

        # print(data)

        # Convert API response data to formatted DataFrame
        formatted_data = pd.DataFrame(data, columns=[
            "Timestamp", "Open", "High", "Low", "Close", "Volume"
        ])
        formatted_data["Timestamp"] = pd.to_datetime(formatted_data["Timestamp"])
        formatted_data["Open"] = formatted_data["Open"].astype(float)
        formatted_data["High"] = formatted_data["High"].astype(float)
        formatted_data["Low"] = formatted_data["Low"].astype(float)
        formatted_data["Close"] = formatted_data["Close"].astype(float)
        formatted_data["Volume"] = formatted_data["Volume"].astype(float)

        # Prepare the file path
        csv_file_name = f"{symbol}_{interval}_candle_data.csv"
        csv_dir = f"C:/Documents/GitHub/AngelOne/historical files/{interval}"
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        
        csv_file_path = os.path.join(csv_dir, csv_file_name)

        # Read existing data if file exists
        existing_data = pd.DataFrame()
        if os.path.exists(csv_file_path):
            existing_data = pd.read_csv(csv_file_path)

        # Convert timestamps to datetime for comparison
        start_timestamp = pd.to_datetime(start_date).tz_localize('UTC').tz_convert('Asia/Kolkata')
        end_timestamp = pd.to_datetime(end_date).tz_localize('UTC').tz_convert('Asia/Kolkata')

        # Filter out existing data within the date range
        if not existing_data.empty:
            existing_data['Timestamp'] = pd.to_datetime(existing_data['Timestamp'])
            mask = (existing_data['Timestamp'] >= start_timestamp) & (existing_data['Timestamp'] <= end_timestamp)
            existing_data = existing_data[~mask]

        # Remove duplicates from new_data keeping the second occurrence
        formatted_data = formatted_data[formatted_data.duplicated(subset=['Timestamp'], keep='last') == False]
        # print(formatted_data)
        # Combine existing data with new data
        combined_data = pd.concat([existing_data, formatted_data], ignore_index=True).sort_values(by='Timestamp')
        # print(combined_data)
        # Write combined data back to the CSV file
        try:
            combined_data.to_csv(csv_file_path, index=False)
            print(f"Data from {start_date} to {end_date} updated in {csv_file_name}")
        except Exception as e:
            print(f"Error occurred while writing CSV: {str(e)}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Angel Broking data: {e}")
