# Normal orders placed here
# *********************************

import http.client
import json
import requests
import certifi

# Specify the path to the CA certificates file
ca_file = certifi.where()
print(certifi.where())

# Create an HTTPSConnection with the specified CA certificates file
conn = http.client.HTTPSConnection(
    'apiconnect.angelbroking.com',
    context=http.client.ssl._create_default_https_context(cafile=ca_file)
)

payload = {
"variety":"NORMAL",
"tradingsymbol":"SBIN-EQ",
"symboltoken":"3045",
"transactiontype":"BUY",
"exchange":"NSE",
"ordertype":"MARKET",
"producttype":"INTRADAY",
"duration":"DAY",
"price":"194.50",
"squareoff":"0",
"stoploss":"0",
"quantity":"1"
}

payload_str = json.dumps(payload)

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6Iks0MjM3MTAiLCJyb2xlcyI6MCwidXNlcnR5cGUiOiJVU0VSIiwidG9rZW4iOiJleUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKemRXSWlPaUpMTkRJek56RXdJaXdpWlhod0lqb3hOekV5TlRrM09UTXlMQ0pwWVhRaU9qRTNNVEkxTURFeU56QXNJbXAwYVNJNkltWTBOMkU1WTJNMExXSmpPR1V0TkRnMU5pMDROVGsxTFROaU5qZGxOak5tWkdSbU5pSXNJbTl0Ym1WdFlXNWhaMlZ5YVdRaU9qWXNJbk52ZFhKalpXbGtJam9pTXlJc0luVnpaWEpmZEhsd1pTSTZJbU5zYVdWdWRDSXNJblJ2YTJWdVgzUjVjR1VpT2lKMGNtRmtaVjloWTJObGMzTmZkRzlyWlc0aUxDSm5iVjlwWkNJNk5pd2ljMjkxY21ObElqb2lNeUlzSW1SbGRtbGpaVjlwWkNJNklqUmlZV0psT1RGaExUYzVZVGt0TXpoa05pMDRNelZrTFRnNE56QTJNMlExTTJRM055SXNJbUZqZENJNmUzMTkuRWxMcVBDWkZuNlNDMHEzYzlxTU5LOFRoVVVubWlpZWlRbzMyTE1FQjVoREx6UHR1TlU2Q1VvSHJCNmliLUVyUS1ZWEhlRGpnTmJZOGczWTUtUS1OUGciLCJBUEktS0VZIjoiMkQ5NWhrQUEiLCJpYXQiOjE3MTI1MDEzMzAsImV4cCI6MTcxMjU5NzkzMn0.4WJAO6Ja3PmxgFgTubn_09_ER7aXLZNw4oBDbFACamCWin2DswGf1CRM6EdXtwNorm9tr0-2a1Yh_z70E52EQA',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-UserType': 'USER',
    'X-SourceID': 'WEB',
    'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
    'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
    'X-MACAddress': 'MAC_ADDRESS',
    'X-PrivateKey': '2D95hkAA'
}

conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", payload_str,headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
