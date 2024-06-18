import requests
import certifi
import csv
import json
import http.client
from headers import headers 

def myholdings():
    # Make the GET request using certifi for SSL certificate verification
    response = requests.get("https://apiconnect.angelbroking.com/rest/secure/angelbroking/portfolio/v1/getHolding", headers=headers, verify=certifi.where())

    # Check if the response status is OK (200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if the response status is true
        if data.get('status'):
            holdings = data.get('data')

            # Define the CSV file path
            csv_file = 'holdings.csv'

            # Display the holdings data in a formatted way
            for holding in holdings:
                print(f"Trading Symbol: {holding['tradingsymbol']}")
                print(f"Exchange: {holding['exchange']}")
                print(f"Quantity: {holding['quantity']}")
                print(f"Product: {holding['product']}")
                print(f"Average Price: {holding['averageprice']}")
                print(f"LTP: {holding['ltp']}")
                print(f"Profit and Loss: {holding['profitandloss']}")
                print("----------------------------")

            # Write the holdings data to a CSV file
            with open(csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Trading Symbol', 'Exchange', 'Quantity', 'Product', 'Average Price', 'LTP', 'Profit and Loss'])
                for holding in holdings:
                    writer.writerow([
                        holding['tradingsymbol'],
                        holding['exchange'],
                        holding['quantity'],
                        holding['product'],
                        holding['averageprice'],
                        holding['ltp'],
                        holding['profitandloss']
                    ])
            print(f"Holdings data saved to {csv_file} successfully.")


        else:
            print("Failed to fetch holdings. Error message:", data.get('message', 'Unknown error'))
    else:
        print("Failed to fetch holdings. HTTP status code:", response.status_code)


def all_myholdings():
    # Make the GET request using certifi for SSL certificate verification
    response = requests.get("https://apiconnect.angelbroking.com/rest/secure/angelbroking/portfolio/v1/getAllHolding", headers=headers, verify=certifi.where())

    # Check if the response status is OK (200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if the response status is true
        if data.get('status'):
            holdings = data.get('data').get('holdings')

            # Define the CSV file path
            csv_file = 'holdings.csv'

            # Display the holdings data in a formatted way
            for holding in holdings:
                print(f"Trading Symbol: {holding['tradingsymbol']}")
                print(f"Exchange: {holding['exchange']}")
                print(f"Quantity: {holding['quantity']}")
                print(f"Product: {holding['product']}")
                print(f"Average Price: {holding['averageprice']}")
                print(f"LTP: {holding['ltp']}")
                print(f"Profit and Loss: {holding['profitandloss']}")
                print("----------------------------")

            totalholding = data.get('data').get('totalholding')
            print(f"Total Holding Value : {totalholding['totalholdingvalue']}")
            print(f"Total Invested Value : {totalholding['totalinvvalue']}")
            print(f"Total Profit And Loss : {totalholding['totalprofitandloss']}")
            print(f"Total Profit And Loss Percentage : {totalholding['totalpnlpercentage']}")

            # Write the holdings data to a CSV file
            with open(csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Trading Symbol', 'Exchange', 'Quantity', 'Product', 'Average Price', 'LTP', 'Profit and Loss'])

                # Write individual holdings
                for holding in holdings:
                    writer.writerow([
                        holding['tradingsymbol'],
                        holding['exchange'],
                        holding['quantity'],
                        holding['product'],
                        holding['averageprice'],
                        holding['ltp'],
                        holding['profitandloss']
                    ])
                
                # Write total holding information as a separate row
                totalholding = data.get('data').get('totalholding')
                writer.writerow([])  # Empty row for separation
                writer.writerow(['Total Holding Value', 'Total Invested Value', 'Total Profit And Loss', 'Total Profit And Loss Percentage'])
                writer.writerow([
                    totalholding['totalholdingvalue'],
                    totalholding['totalinvvalue'],
                    totalholding['totalprofitandloss'],
                    f"{totalholding['totalpnlpercentage']}%"
                ])
            print()
            print(f"Holdings data saved to {csv_file} successfully.")
            print()

        else:
            print("Failed to fetch holdings. Error message:", data.get('message', 'Unknown error'))
    else:
        print("Failed to fetch holdings. HTTP status code:", response.status_code)


def get_position():
    conn = http.client.HTTPSConnection('apiconnect.angelbroking.com')
    conn.request("GET", "/rest/secure/angelbroking/order/v1/getPosition", "", headers)
    res = conn.getresponse()
    data = res.read()
    print("Get Position Response:")
    print(data.decode("utf-8"))


def convert_position():
    conn = http.client.HTTPSConnection('apiconnect.angelbroking.com')
    payload = {
        "exchange": "NSE",
        "symboltoken": "2885",
        "producttype": "DELIVERY",
        "newproducttype": "INTRADAY",
        "tradingsymbol": "RELIANCE-EQ",
        "symbolname": "RELIANCE",
        "instrumenttype": "",
        "priceden": "1",
        "pricenum": "1",
        "genden": "1",
        "gennum": "1",
        "precision": "2",
        "multiplier": "-1",
        "boardlotsize": "1",
        "buyqty": "1",
        "sellqty": "0",
        "buyamount": "2235.80",
        "sellamount": "0",
        "transactiontype": "BUY",
        "quantity": 1,
        "type": "DAY"
    }
    payload_str = json.dumps(payload)
    conn.request("POST", "/rest/secure/angelbroking/order/v1/convertPosition", payload_str, headers)
    res = conn.getresponse()
    data = res.read()
    print("Position Conversion Response:")
    print(data.decode("utf-8"))


