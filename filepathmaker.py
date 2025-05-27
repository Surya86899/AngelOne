import csv

COMPANY_LIST = ['nifty50.csv', 'niftynext50.csv', 'niftymidcap50.csv']
i=0
for company in COMPANY_LIST:
    with open(company, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            for company in row:
                # if company == 'LTF':
                    # continue
                print(f'r"C:\\Documents\\GitHub\\AngelOne\\historical files\\FIFTEEN_MINUTE\\{company}-EQ_FIFTEEN_MINUTE_candle_data.csv",  #{i}')
                i = i + 1