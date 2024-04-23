# Normal orders placed here
# *********************************
from headers import headers
import http.client
import json
import certifi

def create_normal_order(variety,trading_symbol,symbol_token,transaction_type,exchange,order_type,product_type,duration,price,square_off,stop_loss,qty):
    # Specify the path to the CA certificates file
    ca_file = certifi.where()
    print(certifi.where())

    # Create an HTTPSConnection with the specified CA certificates file
    conn = http.client.HTTPSConnection(
        'apiconnect.angelbroking.com',
        context=http.client.ssl._create_default_https_context(cafile=ca_file)
    )

    payload = {
    "variety":variety,
    "tradingsymbol":trading_symbol,
    "symboltoken":symbol_token,
    "transactiontype":transaction_type,
    "exchange":exchange,
    "ordertype":order_type,
    "producttype":product_type,
    "duration":duration,
    "price":price,
    "squareoff":square_off,
    "stoploss":stop_loss,
    "quantity":qty
    }

    payload_str = json.dumps(payload)

    conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", payload_str,headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    response_json = json.loads(data)
    unique_order_id = response_json['data']['uniqueorderid']  # Accessing uniqueorderid from the response

    return unique_order_id

# ****************************Normal Order Modification****************************
def modify_normal_order(variety,order_id,order_type,product_type,duration,price,qty):

    conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

    payload = {
        "variety": variety,
        "orderid": order_id,
        "ordertype": order_type,
        "producttype": product_type,
        "duration": duration,
        "price": price,
        "quantity": qty
    }

    conn.request("POST", "/rest/secure/angelbroking/order/v1/modifyOrder", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

# ****************************Normal Order Cancellation****************************
def cancel_normal_order(variety,order_id):
    import http.client
    import json

    conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

    payload = {
        "variety": variety,
        "orderid": order_id
    }

    conn.request("POST", "/rest/secure/angelbroking/order/v1/cancelOrder", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


#  The order book typically contains information about all open orders placed by a user, including details such as order ID, order type, product type, quantity, price, and status.
def get_normal_orderbook():

    conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

    conn.request("GET", "/rest/secure/angelbroking/order/v1/getOrderBook", "", headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


# The trade book contains information about executed trades, including details such as trade ID, order ID, exchange, symbol, transaction type (buy/sell), quantity, price, timestamp, and other relevant information about each trade.
def get_normal_tradebook():

    conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

    conn.request("GET", "/rest/secure/angelbroking/order/v1/getTradeBook","", headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


# ****************************loss or profit of all trades****************************
def get_ltp_data(exchange,trading_symbol,symbol_token):

    conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

    payload = {
        "exchange": exchange,
        "tradingsymbol": trading_symbol,
        "symboltoken": symbol_token
    }

    conn.request("POST", "/rest/secure/angelbroking/order/v1/getLtpData", json.dumps(payload), headers)

    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

# ****************************Normal Order details****************************
def get_normal_individualorder(unique_order_id):

    conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

    conn.request("GET", f"/rest/secure/angelbroking/order/v1/details/{unique_order_id}", "", headers)

    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))



