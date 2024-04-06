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
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6Iks0MjM3MTAiLCJyb2xlcyI6MCwidXNlcnR5cGUiOiJVU0VSIiwidG9rZW4iOiJleUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKemRXSWlPaUpMTkRJek56RXdJaXdpWlhod0lqb3hOekV4TnpFNU1UWXdMQ0pwWVhRaU9qRTNNVEUyTWpNeE1EUXNJbXAwYVNJNklqazJabVEwWldRNUxXTmlPR1F0TkRnMU1pMDRaR1UwTFRWbE5tTmxZVGxrTlRObFpTSXNJbTl0Ym1WdFlXNWhaMlZ5YVdRaU9qWXNJbk52ZFhKalpXbGtJam9pTXlJc0luVnpaWEpmZEhsd1pTSTZJbU5zYVdWdWRDSXNJblJ2YTJWdVgzUjVjR1VpT2lKMGNtRmtaVjloWTJObGMzTmZkRzlyWlc0aUxDSm5iVjlwWkNJNk5pd2ljMjkxY21ObElqb2lNeUlzSW1SbGRtbGpaVjlwWkNJNklqUmlZV0psT1RGaExUYzVZVGt0TXpoa05pMDRNelZrTFRnNE56QTJNMlExTTJRM055SXNJbUZqZENJNmUzMTkub0tCSG1menVSWnpHVlM4dTlFOE5sSTJ5LU8wTTBBdUJnSXRJMWZWbWlYeXFwekhqSHNGVFM5RlZ6dnVvdTNTZnlUdk1FLUlIMVR5Nk9ZTVI5b3hWN0EiLCJBUEktS0VZIjoiMkQ5NWhrQUEiLCJpYXQiOjE3MTE2MjMxNjQsImV4cCI6MTcxMTcxOTE2MH0.Z9MV3CH0Vj7vrGoLhrmQEYNTaq4c3IcA8T6EsPSO3G_vrn6eO8NkOMDP8sKXRw4-Us5_YIyxo_AImpzhDtsssw', # Jab bhi mai login karunga mujhe ek AUTHORIZATION_TOKEN milega usse daal kar mai sab kuch access kar paunga.
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
