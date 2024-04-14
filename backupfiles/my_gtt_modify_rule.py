#  To modify gtt rules
# ************************************
# Good Till Triggered

import http.client
import certifi
from headers import headers 

# Specify the path to the CA certificates file
ca_file = certifi.where()
print(certifi.where())

# Create an HTTPSConnection with the specified CA certificates file
conn = http.client.HTTPSConnection(
    'apiconnect.angelbroking.com',
    context=http.client.ssl._create_default_https_context(cafile=ca_file)
)

#gtt rule banate wakt ye id milta hai
payload = '''{
    "id": "2819079", 
    "symboltoken": "3045",
    "exchange": "NSE",
    "price": "1000",
    "qty": "100",
    "triggerprice": "755.55",
    "disclosedqty": "10",
    "timeperiod": "20"
}'''


conn.request("POST", "/rest/secure/angelbroking/gtt/v1/modifyRule", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))