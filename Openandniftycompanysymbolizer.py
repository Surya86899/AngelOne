import csv

nifty150_file = 'nifty150.csv'
open_api_file = 'OpenApiScript.csv'

# Step 1: Read symbols from nifty150.csv
nifty150_symbols = []
with open(nifty150_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        nifty150_symbols.append(row[0])  # Assuming symbols are in the first column

# Accumulate filtered data
filtered_data = []
for symbol in nifty150_symbols:
    with open(open_api_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['name'] == symbol and row['symbol'].endswith('-EQ'):
                filtered_data.append({
                    'name': row['name'],
                    'symbol': row['symbol'],
                    'token': row['token']
                })

# Step 2: Append filtered data to nifty150.csv
with open(nifty150_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write header if file is empty
    if file.tell() == 0:
        writer.writerow(['name', 'symbol', 'token'])
    
    # Write filtered data
    for data in filtered_data:
        writer.writerow([data['name'], data['symbol'], data['token']])

print("Filtered data appended to nifty150.csv.")


# Assuming the CSV file structure has columns named 'symbol' and 'token'

with open("nifty150.csv", mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        symbol = row['symbol']
        token = row['token']
        # Assuming you want to print each line in the format "symbol":token
        print(f'"{symbol[:-3]}":{token},')


