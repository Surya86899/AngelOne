import http.client
import requests
import certifi
from logzero import logger
from SmartApi import SmartConnect

# Specify the path to the CA certificates file
ca_file = certifi.where()

api_key = '2D95hkAA'
smartApi = SmartConnect(api_key)

payload = {
    "exchange": "NSE",
    "symboltoken": "3045",
    "interval": "ONE_DAY",
    "fromdate": "2024-03-27 09:00",
    "todate": "2023-03-27 15:30"
}

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6Iks0MjM3MTAiLCJyb2xlcyI6MCwidXNlcnR5cGUiOiJVU0VSIiwidG9rZW4iOiJleUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKemRXSWlPaUpMTkRJek56RXdJaXdpWlhod0lqb3hOekV5TkRnMk5EZzFMQ0pwWVhRaU9qRTNNVEl6T0RVM05qQXNJbXAwYVNJNklqQTBZamxsT1RGa0xUaGhabUl0Tkdaa1l5MDRObVptTFdZM016WTRaREF3WmpnMlppSXNJbTl0Ym1WdFlXNWhaMlZ5YVdRaU9qWXNJbk52ZFhKalpXbGtJam9pTXlJc0luVnpaWEpmZEhsd1pTSTZJbU5zYVdWdWRDSXNJblJ2YTJWdVgzUjVjR1VpT2lKMGNtRmtaVjloWTJObGMzTmZkRzlyWlc0aUxDSm5iVjlwWkNJNk5pd2ljMjkxY21ObElqb2lNeUlzSW1SbGRtbGpaVjlwWkNJNklqUmlZV0psT1RGaExUYzVZVGt0TXpoa05pMDRNelZrTFRnNE56QTJNMlExTTJRM055SXNJbUZqZENJNmUzMTkuNUNuQ1h5eG9JSXJFcFVUU0R6TUFjZHMtbndXYkh3OHRWTk9qUk1vaUduYXlGNWdBdDRRN0RHVjczanZDTGJaTVE4X080VVZ2eEtRLXF5LVdzVlVsOHciLCJBUEktS0VZIjoiMkQ5NWhrQUEiLCJpYXQiOjE3MTIzODU4MjEsImV4cCI6MTcxMjQ4NjQ4NX0.7Aiq0qExHa1yjjYzgCvfEA23opRLdOaH54ZCoQqLTztjArG2kS4DInxMgbywFy3pvTb1hhQ55Ezzs5c5EV0U4w',  # Jab bhi mai login karunga mujhe ek AUTHORIZATION_TOKEN milega usse daal kar mai sab kuch access kar paunga.
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-UserType': 'USER',
    'X-SourceID': 'WEB',
    'X-ClientLocalIP': '192.168.0.105',
    'X-ClientPublicIP': '192.168.0.105',
    'X-MACAddress': '50-C2-E8-8F-5A-85',
    'X-PrivateKey': '2D95hkAA'
}

# Request to get candle data
response = requests.post("https://apiconnect.angelbroking.com/rest/secure/angelbroking/historical/v1/getCandleData", json=payload, headers=headers)

if response.status_code == 200:
    print(response.json())  # Print or do something with the response data
else:
    print("Failed to get candle data")

try:
    historicParam={
    "exchange": "NSE",
    "symboltoken": "3045",
    "interval": "ONE_MINUTE",
    "fromdate": "2021-02-08 09:00", 
    "todate": "2021-02-08 09:16"
    }
    print(smartApi.getCandleData(historicParam))
except Exception as e:
    logger.exception(f"Historic Api failed: {e}")
