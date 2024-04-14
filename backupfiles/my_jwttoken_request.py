import http.client
import certifi

# Specify the path to the CA certificates file
ca_file = certifi.where()

# Create an HTTPSConnection with the specified CA certificates file
conn = http.client.HTTPSConnection(
    'apiconnect.angelbroking.com',
    context=http.client.ssl._create_default_https_context(cafile=ca_file)
)

payload = """{
    "refreshToken": "eyJhbGciOiJIUzUxMiJ9.eyJ0b2tlbiI6IlJFRlJFU0gtVE9LRU4iLCJSRUZSRVNILVRPS0VOIjoiZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnpkV0lpT2lKTE5ESXpOekV3SWl3aVpYaHdJam94TnpFeU5Ea3dOalk0TENKcFlYUWlPakUzTVRJME1EUXlNRGdzSW1wMGFTSTZJak0wTnpJNU56Y3hMV0ptTXpZdE5EUTFPUzFpTWpaaUxUUmhNbUk1TkdJeU5HSTNZU0lzSW05dGJtVnRZVzVoWjJWeWFXUWlPakFzSW5SdmEyVnVJam9pVWtWR1VrVlRTQzFVVDB0RlRpSXNJblZ6WlhKZmRIbHdaU0k2SW1Oc2FXVnVkQ0lzSW5SdmEyVnVYM1I1Y0dVaU9pSjBjbUZrWlY5eVpXWnlaWE5vWDNSdmEyVnVJaXdpWkdWMmFXTmxYMmxrSWpvaVlUUm1NREJoWVdVdFl6UTVaQzB6WXpaakxUaGxObVV0WVdNNE9HWm1ZVGN3T1RReUlpd2lZV04wSWpwN2ZYMC5UZ1ROWTIxa0dRWHEtUmpiN04wTUljZFAtNWNhYVFac2lBYk1QREwxejhxUkxCMERVR2NGWFIyVkhwZlF1UGtJTHVjcW1VRllpM2lfcHhPZEhZcVNUQSIsImlhdCI6MTcxMjQwNDI2OH0.h2W3TCYseRAyR8e7lDnaGxWPlXP3WG3qL8bB8KYcxZXP7iM58VKrd4INorNCOaIY2beIF2e_Pw4g0QMt7uFihA"
}"""

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6Iks0MjM3MTAiLCJyb2xlcyI6MCwidXNlcnR5cGUiOiJVU0VSIiwidG9rZW4iOiJleUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKemRXSWlPaUpMTkRJek56RXdJaXdpWlhod0lqb3hOekV5TlRBeE1ETTNMQ0pwWVhRaU9qRTNNVEkwTURReU1EZ3NJbXAwYVNJNkltVTJOVFU0TldJMExUQmlabUl0TkRFNE1pMWhNemM0TFRBMFpEZG1aRFEwT0RneVpTSXNJbTl0Ym1WdFlXNWhaMlZ5YVdRaU9qWXNJbk52ZFhKalpXbGtJam9pTXlJc0luVnpaWEpmZEhsd1pTSTZJbU5zYVdWdWRDSXNJblJ2YTJWdVgzUjVjR1VpT2lKMGNtRmtaVjloWTJObGMzTmZkRzlyWlc0aUxDSm5iVjlwWkNJNk5pd2ljMjkxY21ObElqb2lNeUlzSW1SbGRtbGpaVjlwWkNJNkltRTBaakF3WVdGbExXTTBPV1F0TTJNMll5MDRaVFpsTFdGak9EaG1abUUzTURrME1pSXNJbUZqZENJNmUzMTkuRjR4U283cHdsZXUwU09EWHRqNlEyRHdxd1VBQUVxYVV6WmtIRHhKSFpkYk5mYUZWUXRBWHE4TXFCU2VCYXBkaEhwZ1BNbjRYbmxXTWhxbG5PRENjeEEiLCJBUEktS0VZIjoiS1BZSms2TmwiLCJpYXQiOjE3MTI0MDQyNjgsImV4cCI6MTcxMjUwMTAzN30.4LpKRDVAIA_m5x6SArGrdILWwAuqKCYAbiFL76GREgek-58uu3-uWtc8WA93WVBBCIaTXu4EkDqNc71lDCiynw', # Jab bhi mai login karunga mujhe ek AUTHORIZATION_TOKEN milega usse daal kar mai sab kuch access kar paunga.
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-UserType': 'USER',
    'X-SourceID': 'WEB',
    'X-ClientLocalIP': '192.168.0.105',
    'X-ClientPublicIP': '192.168.0.105',
    'X-MACAddress': '50-C2-E8-8F-5A-85',
    'X-PrivateKey': '2D95hkAA'
}

# Make the POST request
conn.request("POST", "/rest/auth/angelbroking/jwt/v1/generateTokens", payload, headers)

# Get the response
res = conn.getresponse()
data = res.read()

# Print the response
print(data.decode("utf-8"))

