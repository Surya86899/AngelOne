import http.client
import certifi
import json
import csv
import os
from headers import headers

def create_gtt_rule(trading_symbol, symbol_token, exchange, transaction_type, product_type, price, qty, trigger_price, disclosed_qty, time_period):
    # Specify the path to the CA certificates file
    ca_file = certifi.where()

    # Create an HTTPSConnection with the specified CA certificates file
    conn = http.client.HTTPSConnection(
        'apiconnect.angelbroking.com',
        context=http.client.ssl._create_default_https_context(cafile=ca_file)
    )

    # Prepare the payload
    payload = {
        "tradingsymbol": trading_symbol,
        "symboltoken": symbol_token,
        "exchange": exchange,
        "transactiontype": transaction_type,
        "producttype": product_type,
        "price": price,
        "qty": qty,
        "triggerprice": trigger_price,
        "disclosedqty": disclosed_qty,
        "timeperiod": time_period
    }

    # Make the POST request
    conn.request("POST", "/rest/secure/angelbroking/gtt/v1/createRule", json.dumps(payload), headers)

    # Get the response
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    
    # Parse the response data
    response_data = json.loads(data)
    
    # Extract the ID of the created rule
    rule_id = response_data.get("data", {}).get("id")

    # Append the rule parameters and ID to a CSV file
    with open("gtt_rules.csv", "a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([rule_id, trading_symbol, symbol_token, transaction_type, product_type, price, qty, time_period])

    return rule_id

# Define function to modify GTT rule
def modify_gtt_rule(rule_id, trading_symbol, symbol_token, exchange, transaction_type, product_type, price, qty, trigger_price, disclosed_qty, time_period):
    # Specify the path to the CA certificates file
    ca_file = certifi.where()

    # Create an HTTPSConnection with the specified CA certificates file
    conn = http.client.HTTPSConnection(
        'apiconnect.angelbroking.com',
        context=http.client.ssl._create_default_https_context(cafile=ca_file)
    )

    # Construct the payload with the rule ID and updated parameters
    payload = {
        "id": rule_id,
        "tradingsymbol": trading_symbol,
        "symboltoken": symbol_token,
        "exchange": exchange,
        "transactiontype": transaction_type,
        "producttype": product_type,
        "price": price,
        "qty": qty,
        "triggerprice": trigger_price,
        "disclosedqty": disclosed_qty,
        "timeperiod": time_period
    }

    # Make the POST request to modify the GTT rule
    conn.request("POST", "/rest/secure/angelbroking/gtt/v1/modifyRule", json.dumps(payload), headers)

    # Get the response
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    # Parse the response data
    response_data = json.loads(data)

    # Check if modification was successful
    if response_data.get("status") == True:
        # Read existing entries from the CSV file
        with open("gtt_rules.csv", "r", newline="") as csv_file:
            reader = csv.reader(csv_file)
            lines = list(reader)

        # Find the line with the corresponding rule ID and update it
        for i, line in enumerate(lines):
            if line[0] == str(rule_id):
                lines[i] = [str(rule_id), trading_symbol,symbol_token,transaction_type,product_type,price,qty,time_period]
                break

        # Write the updated lines back to the CSV file
        with open("gtt_rules.csv", "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(lines)

    # Print the response
    print(data)

# Define function to get GTT rule details
def get_gtt_rule_details(rule_id):
    # Specify the path to the CA certificates file
    ca_file = certifi.where()

    # Create an HTTPSConnection with the specified CA certificates file
    conn = http.client.HTTPSConnection(
        'apiconnect.angelbroking.com',
        context=http.client.ssl._create_default_https_context(cafile=ca_file)
    )

    # Construct the payload with the rule ID
    payload = {
        "id": rule_id
    }

    # Make the POST request to retrieve details of the GTT rule
    conn.request("POST", "/rest/secure/angelbroking/gtt/v1/ruleDetails", json.dumps(payload), headers)

    # Get the response
    res = conn.getresponse()
    data = res.read()

    # Print the response
    print(data.decode("utf-8"))

# Define function to get all GTT rule details
def get_gtt_allrule_details():
    # Specify the path to the CA certificates file
    ca_file = certifi.where()

    # Create an HTTPSConnection with the specified CA certificates file
    conn = http.client.HTTPSConnection(
        'apiconnect.angelbroking.com',
        context=http.client.ssl._create_default_https_context(cafile=ca_file)
    )

    # Define the payload
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

    # Make the POST request
    conn.request("POST", "/rest/secure/angelbroking/gtt/v1/ruleList", payload, headers)

    # Get the response
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    # Parse the JSON response
    response_data = json.loads(data)

    # Print the details with a line space between each order
    for order in response_data["data"]:
        print(json.dumps(order, indent=4))
        print()  # Add a line space between orders

# Define function to cancel GTT rule
def cancel_gtt_rule(rule_id,symbol_token,ex_change):
    # Specify the path to the CA certificates file
    ca_file = certifi.where()

    # Create an HTTPSConnection with the specified CA certificates file
    conn = http.client.HTTPSConnection(
        'apiconnect.angelbroking.com',
        context=http.client.ssl._create_default_https_context(cafile=ca_file)
    )

    # Construct the payload with the rule ID
    payload = {
        "id": rule_id,    
        "symboltoken": symbol_token,
        "exchange": ex_change
    }

    # Make the POST request to cancel the GTT rule
    conn.request("POST", "/rest/secure/angelbroking/gtt/v1/cancelRule", json.dumps(payload), headers)

    # Get the response
    res = conn.getresponse()
    data = res.read()

    # Decode the response body from bytes to a Python dictionary
    response_data = json.loads(data.decode("utf-8"))

    # Check if the cancellation request was successful
    if response_data.get("status") == True:
        # Print the response
        print(data.decode("utf-8"))

        # Modify the CSV file to remove the cancelled rule
        input_file = 'gtt_rules.csv'
        temp_file = 'temp_gtt_rules.csv'

        # Read the CSV file and store its data
        with open(input_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Remove the row with the specified ID
        modified_rows = [row for row in rows if row['id'] != rule_id]

        # Write the modified data to a temporary file
        with open(temp_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(modified_rows)

        # Replace the original file with the temporary file
        os.replace(temp_file, input_file)

        # Print a message indicating the cancellation
        print(f"GTT rule with ID {rule_id} has been successfully cancelled.")
    else:
        # Print an error message if the cancellation request failed
        print(f"Failed to cancel GTT rule with ID {rule_id}. Error: {data.decode('utf-8')}")
