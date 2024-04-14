# import requests
# import csv

# # Endpoint URL
# url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"

# # Send GET request to the endpoint
# response = requests.get(url)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Parse JSON response
#     scrips = response.json()

#     # Save data to a CSV file
#     with open("OpenAPIScripMaster.csv", "w", newline='', encoding='utf-8') as csvfile:
#         fieldnames = scrips[0].keys() if scrips else []
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#         writer.writeheader()
#         for scrip in scrips:
#             writer.writerow(scrip)

#     print("CSV file downloaded successfully as OpenAPIScripMaster.csv")
# else:
#     print(f"Failed to download CSV file. Status code: {response.status_code}")
