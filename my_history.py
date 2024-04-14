import requests
import certifi
import csv

# Specify the path to the CA certificates file
ca_file = certifi.where()

# Request to get candle data
payload = {
    "exchange": "NSE",
    "symboltoken": "3045",
    "interval": "ONE_DAY",
    "fromdate": "2024-03-27 09:00",
    "todate": "2024-04-08 03:30"
}

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6Iks0MjM3MTAiLCJyb2xlcyI6MCwidXNlcnR5cGUiOiJVU0VSIiwidG9rZW4iOiJleUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKemRXSWlPaUpMTkRJek56RXdJaXdpWlhod0lqb3hOekV5TlRrM09UTXlMQ0pwWVhRaU9qRTNNVEkxTURFeU56QXNJbXAwYVNJNkltWTBOMkU1WTJNMExXSmpPR1V0TkRnMU5pMDROVGsxTFROaU5qZGxOak5tWkdSbU5pSXNJbTl0Ym1WdFlXNWhaMlZ5YVdRaU9qWXNJbk52ZFhKalpXbGtJam9pTXlJc0luVnpaWEpmZEhsd1pTSTZJbU5zYVdWdWRDSXNJblJ2YTJWdVgzUjVjR1VpT2lKMGNtRmtaVjloWTJObGMzTmZkRzlyWlc0aUxDSm5iVjlwWkNJNk5pd2ljMjkxY21ObElqb2lNeUlzSW1SbGRtbGpaVjlwWkNJNklqUmlZV0psT1RGaExUYzVZVGt0TXpoa05pMDRNelZrTFRnNE56QTJNMlExTTJRM055SXNJbUZqZENJNmUzMTkuRWxMcVBDWkZuNlNDMHEzYzlxTU5LOFRoVVVubWlpZWlRbzMyTE1FQjVoREx6UHR1TlU2Q1VvSHJCNmliLUVyUS1ZWEhlRGpnTmJZOGczWTUtUS1OUGciLCJBUEktS0VZIjoiMkQ5NWhrQUEiLCJpYXQiOjE3MTI1MDEzMzAsImV4cCI6MTcxMjU5NzkzMn0.4WJAO6Ja3PmxgFgTubn_09_ER7aXLZNw4oBDbFACamCWin2DswGf1CRM6EdXtwNorm9tr0-2a1Yh_z70E52EQA',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-UserType': 'USER',
    'X-SourceID': 'WEB',
    'X-ClientLocalIP': '192.168.0.105',
    'X-ClientPublicIP': '192.168.0.105',
    'X-MACAddress': '50-C2-E8-8F-5A-85',
    'X-PrivateKey': '2D95hkAA'  # Replace with your actual private key
}

url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/historical/v1/getCandleData"

response = requests.post(url, json=payload, headers=headers)
data = response.json()

# Extract candle data
candle_data = data.get('data', [])

# Extract symboltoken
symboltoken = payload['symboltoken']

# Define CSV file name
csv_file_name = f"{symboltoken}_candle_data.csv"

# Write candle data to CSV file
if candle_data:
    with open(f"C:\Documents\GitHub\Python\historical files\{csv_file_name}", mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Volume"])
        # Write candle data rows
        for candle in candle_data:
            writer.writerow(candle)

    print(f"Data saved to {csv_file_name}")
else:
    print("No candle data found.")
