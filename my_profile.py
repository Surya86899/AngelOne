import requests
import json

url = 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/user/v1/getProfile'
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6Iks0MjM3MTAiLCJyb2xlcyI6MCwidXNlcnR5cGUiOiJVU0VSIiwidG9rZW4iOiJleUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKemRXSWlPaUpMTkRJek56RXdJaXdpWlhod0lqb3hOekV5TkRnMk5EZzFMQ0pwWVhRaU9qRTNNVEl6T0RVM05qQXNJbXAwYVNJNklqQTBZamxsT1RGa0xUaGhabUl0Tkdaa1l5MDRObVptTFdZM016WTRaREF3WmpnMlppSXNJbTl0Ym1WdFlXNWhaMlZ5YVdRaU9qWXNJbk52ZFhKalpXbGtJam9pTXlJc0luVnpaWEpmZEhsd1pTSTZJbU5zYVdWdWRDSXNJblJ2YTJWdVgzUjVjR1VpT2lKMGNtRmtaVjloWTJObGMzTmZkRzlyWlc0aUxDSm5iVjlwWkNJNk5pd2ljMjkxY21ObElqb2lNeUlzSW1SbGRtbGpaVjlwWkNJNklqUmlZV0psT1RGaExUYzVZVGt0TXpoa05pMDRNelZrTFRnNE56QTJNMlExTTJRM055SXNJbUZqZENJNmUzMTkuNUNuQ1h5eG9JSXJFcFVUU0R6TUFjZHMtbndXYkh3OHRWTk9qUk1vaUduYXlGNWdBdDRRN0RHVjczanZDTGJaTVE4X080VVZ2eEtRLXF5LVdzVlVsOHciLCJBUEktS0VZIjoiMkQ5NWhrQUEiLCJpYXQiOjE3MTIzODU4MjEsImV4cCI6MTcxMjQ4NjQ4NX0.7Aiq0qExHa1yjjYzgCvfEA23opRLdOaH54ZCoQqLTztjArG2kS4DInxMgbywFy3pvTb1hhQ55Ezzs5c5EV0U4w', # Jab bhi mai login karunga mujhe ek AUTHORIZATION_TOKEN milega usse daal kar mai sab kuch access kar paunga.
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-UserType': 'USER',
    'X-SourceID': 'WEB',
    'X-ClientLocalIP': '192.168.0.105',
    'X-ClientPublicIP': '192.168.0.105',
    'X-MACAddress': '50-C2-E8-8F-5A-85',
    'X-PrivateKey': '2D95hkAA'
}

try:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    print(json.dumps(response_data, indent=2))
except Exception as e:
    print(f"An error occurred: {e}")
