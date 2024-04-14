import requests
import certifi
import csv
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
