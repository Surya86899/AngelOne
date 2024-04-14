#  To create gtt rule
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

# qty = jo actual quantity hame kharidna hai
# disclosedqty = ek time mai jitna hame kharidna hai
# eg A wants to take 1000 shares then (qty = 1000) and he does not want market to know abt it so he uses (disclosedqty = 100) which means he will take 100 shares in single order and it will repeat till he takes 1000 shares

payload = """
{
    "tradingsymbol": "SBIN-EQ",
    "symboltoken": "3045",
    "exchange": "NSE",
    "transactiontype": "BUY",
    "producttype": "DELIVERY",
    "price": "754",
    "qty": "50",
    "triggerprice": "753.95",
    "disclosedqty": "50",
    "timeperiod": "20"
}
"""

# Make the POST request
conn.request("POST", "/rest/secure/angelbroking/gtt/v1/createRule", payload, headers)

# Get the response
res = conn.getresponse()
data = res.read()

# Print the response
print(data.decode("utf-8"))

