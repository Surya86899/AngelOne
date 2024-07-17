# Code for downloading OpenApiScript that contains stock details
 
import http.client
import json
import csv
import time

# Create a connection to the server
conn = http.client.HTTPSConnection("margincalculator.angelbroking.com")

# Define the endpoint for the request
endpoint = "/OpenAPI_File/files/OpenAPIScripMaster.json"

try:
    start_time = time.time()
    
    # Send the GET request
    conn.request("GET", endpoint)
    print("Request sent to server...")

    # Get the response from the server
    res = conn.getresponse()
    if res.status != 200:
        raise Exception(f"Failed to fetch data: {res.status} {res.reason}")
    data = res.read()
    
    fetch_time = time.time()
    print(f"Data fetched in {fetch_time - start_time:.2f} seconds")

    # Decode the response from bytes to string
    decoded_data = data.decode("utf-8")
    
    decode_time = time.time()
    print(f"Data decoded in {decode_time - fetch_time:.2f} seconds")

    # Parse the JSON response
    instruments = json.loads(decoded_data)
    parse_time = time.time()
    print(f"Data parsed in {parse_time - decode_time:.2f} seconds")

    # Print the number of instruments
    print(f"Number of instruments: {len(instruments)}")

    # Define the CSV file name
    csv_file_name = 'OpenApiScript.csv'

    # Write the JSON data to a CSV file
    with open(csv_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        header = [
            "token", "symbol", "name", "expiry", "strike", "lotsize",
            "instrumenttype", "exch_seg", "tick_size"
        ]
        writer.writerow(header)
        
        # Write the data
        for instrument in instruments:
            row = [
                instrument.get("token", ""),
                instrument.get("symbol", ""),
                instrument.get("name", ""),
                instrument.get("expiry", ""),
                instrument.get("strike", ""),
                instrument.get("lotsize", ""),
                instrument.get("instrumenttype", ""),
                instrument.get("exch_seg", ""),
                instrument.get("tick_size", "")
            ]
            writer.writerow(row)

    write_time = time.time()
    print(f"Data written to CSV in {write_time - parse_time:.2f} seconds")
    print(f"Total time taken: {write_time - start_time:.2f} seconds")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    conn.close()
