# Code for downloading combined historical stocks data from AngelOne as well as NSE 
import requests
import os
import csv
import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone
import time

# Assuming these imports are correct
from headers import headers
from nselib.capital_market import capital_market_data

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

def fetch_angel_candle_data(exchange, symbol_token, interval, start_date, end_date, symbol):
    """
    Fetch candle data from Angel Broking API.

    Parameters:
    - exchange (str): Exchange name (e.g., NSE).
    - symbol_token (str): Symbol token for the specific instrument.
    - interval (str): Interval of the candle data (e.g., ONE_DAY).
    - start_date (str): Start date and time in "%Y-%m-%d %H:%M" format.
    - end_date (str): End date and time in "%Y-%m-%d %H:%M" format.
    - symbol (str): Trading symbol of the instrument.

    Returns:
    - list: List of lists containing formatted candle data: [Timestamp, Open, High, Low, Close, Volume].
    """
    time.sleep(1)
    url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/historical/v1/getCandleData"
    # Calculate one day before start_date
    angel_start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M") - timedelta(days=1)
    angel_start_date_str = angel_start_date.strftime("%Y-%m-%d %H:%M")
    
    payload = {
        "exchange": exchange,
        "symboltoken": symbol_token,
        "interval": interval,
        "fromdate": angel_start_date_str,
        "todate": end_date
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json().get('data', [])
        formatted_data = [
            [
                entry[0],  # Timestamp
                float(entry[1]),  # Open
                float(entry[2]),  # High
                float(entry[3]),  # Low
                float(entry[4]),  # Close
                float(entry[5])   # Volume
            ] for entry in data
        ]
        return formatted_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Angel Broking data: {e}")
        return []

def format_date_for_api(date_str):
    """
    Format date for API request in "dd-mm-yyyy" format.

    Parameters:
    - date_str (str): Date string in "%Y-%m-%d" format.

    Returns:
    - str: Formatted date string.
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d-%m-%Y")

def format_date_for_csv(date_str):
    """
    Format date for CSV storage in "%Y-%m-%d" format.

    Parameters:
    - date_str (str): Date string in "%d-%b-%Y %H:%M:%S%z" format.

    Returns:
    - str: Formatted date string.
    """
    date_obj = datetime.strptime(date_str, "%d-%b-%Y %H:%M:%S%z")
    # Convert timezone to +05:30 format
    date_obj = date_obj.astimezone(timezone('Asia/Kolkata'))
    return date_obj.replace(hour=0, minute=0, second=0).strftime("%Y-%m-%d")

def convert_to_float(value):
    """
    Convert a string representation of a float to a float.

    Parameters:
    - value (str): Value to convert.

    Returns:
    - float: Converted float value, or original value if conversion fails.
    """
    if isinstance(value, str):
        try:
            return float(value.replace(',', ''))
        except ValueError:
            return value
    return value

def merge_and_save_data(symbol, exchange1, symbol_token1, interval, start_date, end_date, file2_path):
    """
    Fetch Angel Broking candle data, merge it with NSE data, and save to a CSV file.

    Parameters:
    - symbol (str): Trading symbol of the instrument.
    - exchange1 (str): Exchange name for Angel Broking (e.g., NSE).
    - symbol_token1 (str): Symbol token for Angel Broking API.
    - interval (str): Interval of the candle data (e.g., ONE_DAY).
    - start_date (str): Start date and time in "%Y-%m-%d %H:%M" format.
    - end_date (str): End date and time in "%Y-%m-%d %H:%M" format.
    - file2_path (str): File path for CSV storage.

    """
    angel_data = fetch_angel_candle_data(exchange1, symbol_token1, interval, start_date, end_date, symbol)
    angel_df = pd.DataFrame(angel_data, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
    
    stripped_symbol = symbol[:-3]
    nse_data = capital_market_data.get_price_volume_and_deliverable_position_data(
        symbol=stripped_symbol, 
        from_date=format_date_for_api(start_date.split(' ')[0]), 
        to_date=format_date_for_api(end_date.split(' ')[0])
    )

    formatted_nse_data = []
    for index, row in nse_data.iterrows():
        dly_qty = convert_to_float(row['DeliverableQty'])
        dly_percentage = convert_to_float(row['%DlyQttoTradedQty'])
        if pd.isnull(dly_qty) or pd.isnull(dly_percentage) or dly_qty == '-' or dly_percentage == '-':
            continue
        timestamp = format_date_for_csv(row['Date'] + ' 00:00:00+0530')  # Ensure consistent timezone format and only date part
        formatted_nse_data.append([timestamp, dly_qty, dly_percentage])

    nse_df = pd.DataFrame(formatted_nse_data, columns=["Timestamp", "DLYQty", "DLYPercentage"])

    # Merge based on date part of timestamp
    angel_df['Date'] = pd.to_datetime(angel_df['Timestamp']).dt.date
    nse_df['Date'] = pd.to_datetime(nse_df['Timestamp']).dt.date

    combined_df = pd.merge(angel_df, nse_df, on="Date", how="left")

    # Select only the desired columns in combined_df
    combined_df = combined_df[['Timestamp_x', 'Open', 'High', 'Low', 'Close', 'Volume', 'DLYQty', 'DLYPercentage']]
    combined_df = combined_df.rename(columns={'Timestamp_x': 'Timestamp'})

    # Prepare CSV file path and directory
    csv_file_name = f"{symbol}_{interval}_candle_data.csv"
    csv_dir = "C:/Documents/GitHub/AngelOne/historical files"
    csv_file_path = os.path.join(csv_dir, csv_file_name)

    # Handle existing file or new file creation
    if os.path.exists(csv_file_path):
        existing_data = pd.read_csv(csv_file_path)
        combined_df = pd.concat([existing_data, combined_df], ignore_index=True).drop_duplicates(subset=['Timestamp'], keep='last').sort_values(by='Timestamp')
    else:
        combined_df = combined_df.drop_duplicates(subset=['Timestamp'], keep='last').sort_values(by='Timestamp')

    # Save combined data to CSV
    try:
        combined_df.to_csv(csv_file_path, index=False)
        print(f"Data from {start_date} to {end_date} updated in {csv_file_name}")
    except Exception as e:
        print(f"Error occurred while writing CSV: {str(e)}")


