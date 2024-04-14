#  To get gtt details of all the rules
# ************************************
# Good Till Triggered


import http.client
import certifi

# Specify the path to the CA certificates file
ca_file = certifi.where()
print(certifi.where())

# Create an HTTPSConnection with the specified CA certificates file
conn = http.client.HTTPSConnection(
    'apiconnect.angelbroking.com',
    context=http.client.ssl._create_default_https_context(cafile=ca_file)
)

# Defining the payload
payload = '''{
    "status": [
        "NEW",
        "CANCELLED",
        "ACTIVE",
        "SENTTOEXCHANGE",
        "FORALL"
    ],
    "page": 1,
    "count": 10
}'''

# Defining the headers
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

# Making the POST request
conn.request("POST", "/rest/secure/angelbroking/gtt/v1/ruleList", payload, headers)

# Getting the response
res = conn.getresponse()
data = res.read()

# Printing the response
print(data.decode("utf-8"))
