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
    "refreshToken": "eyJhbGciOiJIUzUxMiJ9.eyJ0b2tlbiI6IlJFRlJFU0gtVE9LRU4iLCJSRUZSRVNILVRPS0VOIjoiZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnpkV0lpT2lKTE5ESXpOekV3SWl3aVpYaHdJam94TnpFeE56RXlNVEEwTENKcFlYUWlPakUzTVRFMk1qVTJORFFzSW1wMGFTSTZJamN4TldNME5HVm1MVE0zTm1RdE5HVm1PUzA1TWpreExXSmtOVFV5WkRJNFpqRTNOU0lzSW05dGJtVnRZVzVoWjJWeWFXUWlPakFzSW5SdmEyVnVJam9pVWtWR1VrVlRTQzFVVDB0RlRpSXNJblZ6WlhKZmRIbHdaU0k2SW1Oc2FXVnVkQ0lzSW5SdmEyVnVYM1I1Y0dVaU9pSjBjbUZrWlY5eVpXWnlaWE5vWDNSdmEyVnVJaXdpWkdWMmFXTmxYMmxrSWpvaU5HSmhZbVU1TVdFdE56bGhPUzB6T0dRMkxUZ3pOV1F0T0RnM01EWXpaRFV6WkRjM0lpd2lZV04wSWpwN2ZYMC5UNjQtS2tESll3UElHbjh2ZDFqMlBjZG9xTTN6Z3BmM1JVN19LSVlObFhNWlM2SmVPTEdIM0R2UnNrZ1huUlB4dERueUVFOXNIbmZzeVFCMDZib011QSIsImlhdCI6MTcxMTYyNTcwNH0.XC_B7JCY8bppKRrilHxC3YdCllM9GA4DcK0uUM7n7byaPZRLRSmwKlE8s_2EAY98aI_8elb9Ma6oRIxnlRzyOQ"
}"""

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

# Make the POST request
conn.request("POST", "/rest/auth/angelbroking/jwt/v1/generateTokens", payload, headers)

# Get the response
res = conn.getresponse()
data = res.read()

# Print the response
print(data.decode("utf-8"))

