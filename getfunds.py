import requests
import http.client
import certifi
from headers import headers
import json

def myfunds():
    # Specify the path to the CA certificates file
    ca_file = certifi.where()
    print(certifi.where())

    # Create an HTTPSConnection with the specified CA certificates file
    conn = http.client.HTTPSConnection(
        'apiconnect.angelbroking.com',
        context=http.client.ssl._create_default_https_context(cafile=ca_file)
    )

    url = 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/user/v1/getRMS'

    conn.request("GET", url, headers=headers)

    res = conn.getresponse()
    data = res.read()
    funds_str = data.decode('utf-8')  # Decode bytes to string
    funds_dict = json.loads(funds_str)  # Parse JSON string to dictionary
    print(data.decode("utf-8"))
    return funds_dict