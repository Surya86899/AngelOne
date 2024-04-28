import requests
import certifi
import csv
import os
from headers import headers  # Assuming headers is correctly defined in the headers module

# Function to search for a symbol and token by name in the OpenAPIScripMaster.csv file
def search_symbol_by_name(name, file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['name'] == name:
                return row['token'], row['symbol']
    return None, None

# Function to retrieve historical candle data
def myhistory(exchange, symbol_token, interval, start_date, end_date, symbol):
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

    # Sending a POST request to the API
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    # Extracting candle data
    candle_data = data.get('data', [])

    # Writing candle data to CSV file
    csv_file_name = f"{symbol}_{interval}_candle_data.csv"
    csv_file_path = os.path.join("C:/Documents/GitHub/AngelOne/historical files", csv_file_name)

    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Writing header row if the file is newly created
        if os.path.getsize(csv_file_path) == 0:
            writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Volume"])
        # Writing candle data rows
        for candle in candle_data:
            writer.writerow(candle)

    if candle_data:
        print(f"Data from {start_date} to {end_date} appended to {csv_file_name}")
    else:
        print("No candle data found.")